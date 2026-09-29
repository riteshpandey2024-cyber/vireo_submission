
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

SLA_MINUTES = {"chat": 15, "voice": 120, "social": 240, "email": 480}
SLA_CREDIT_INR = 350

def _to_ist_naive(series: pd.Series) -> pd.Series:
    # Source timestamps are UTC per the pack.
    return pd.to_datetime(series, errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)

def in_shift(hour: int, shift: str) -> bool:
    if shift == "Morning":
        return 6 <= hour < 14
    if shift == "Day":
        return 14 <= hour < 22
    if shift == "Night":
        return hour >= 22 or hour < 6
    return False

def load_data(data_dir: str | Path):
    d = Path(data_dir)
    tickets = pd.read_csv(d / "tickets.csv")
    agents = pd.read_csv(d / "agents.csv", parse_dates=["from_date", "to_date"])
    customers = pd.read_csv(d / "customers.csv")
    orders = pd.read_csv(d / "orders.csv", parse_dates=["order_date"])
    products = pd.read_csv(d / "products.csv")
    return tickets, agents, customers, orders, products

def prepare_tickets(tickets: pd.DataFrame, agents: pd.DataFrame) -> pd.DataFrame:
    t = tickets.copy()
    t["created_at"] = pd.to_datetime(t["created_at"], errors="coerce")
    t["first_response_at"] = pd.to_datetime(t["first_response_at"], errors="coerce")
    t["resolved_at"] = pd.to_datetime(t["resolved_at"], errors="coerce")
    agents = agents.copy()
    agents["from_date"] = pd.to_datetime(agents["from_date"], errors="coerce")
    agents["to_date"] = pd.to_datetime(agents["to_date"], errors="coerce")

    # Migration re-imports: one analytical row per ticket_id.
    # Prefer the current helpdesk copy when duplicate IDs exist.
    t["_source_rank"] = t["source_system"].map({"helpdesk": 0, "legacy_fd": 1}).fillna(9)
    t = (t.sort_values(["ticket_id", "_source_rank"])
           .drop_duplicates("ticket_id", keep="first")
           .drop(columns="_source_rank")
           .reset_index(drop=True))

    # Keep UTC for SLA elapsed time; use IST only for roster/shift/calendar reporting.
    t["created_ist"] = _to_ist_naive(t["created_at"])
    t["first_response_ist"] = _to_ist_naive(t["first_response_at"])
    t["resolved_ist"] = _to_ist_naive(t["resolved_at"])

    t["response_minutes"] = (t["first_response_at"] - t["created_at"]).dt.total_seconds() / 60
    t["target_minutes"] = t["channel"].map(SLA_MINUTES)
    t["breach"] = t["response_minutes"] > t["target_minutes"]

    # Roster is effective-dated. Match the resolving agent to the assignment
    # effective on the ticket's IST creation date. This is deterministic and,
    # in this dataset, every ticket has exactly one matching assignment.
    def roster_row(row):
        d = row["created_ist"].normalize()
        m = agents[
            (agents["agent_id"] == row["agent_id"]) &
            (agents["from_date"] <= d) &
            (agents["to_date"].fillna(pd.Timestamp.max) >= d)
        ]
        if len(m) != 1:
            raise ValueError(f"Roster match expected 1 row, got {len(m)} for {row['ticket_id']}")
        return m.iloc[0]

    roster = t.apply(roster_row, axis=1)
    for c in ["name", "site", "team", "shift", "tier"]:
        t[c] = roster[c].to_numpy()

    t["week_start"] = t["created_ist"].dt.normalize() - pd.to_timedelta(t["created_ist"].dt.weekday, unit="D")
    t["month"] = t["created_ist"].dt.to_period("M").astype(str)
    t["quarter"] = t["created_ist"].dt.to_period("Q").astype(str)
    t["created_hour_ist"] = t["created_ist"].dt.hour
    t["in_resolver_shift"] = [
        in_shift(int(h), s) for h, s in zip(t["created_hour_ist"], t["shift"])
    ]
    t["carryover_breach"] = t["breach"] & ~t["in_resolver_shift"]

    # Legacy 0 means "no response", not a real CSAT score.
    t["csat_clean"] = t["csat_score"].mask(
        (t["csat_score"] == 0) & (t["source_system"] == "legacy_fd")
    )
    return t

def weekly_report(t: pd.DataFrame, include_tier2=True) -> pd.DataFrame:
    x = t if include_tier2 else t[t["tier"] == 1]
    return (x.groupby(["week_start", "shift", "agent_id", "name", "site", "team", "tier"], dropna=False)
              .agg(
                  tickets=("ticket_id", "size"),
                  breaches=("breach", "sum"),
                  breach_rate=("breach", "mean"),
                  median_response_min=("response_minutes", "median"),
                  carryover_breaches=("carryover_breach", "sum"),
              )
              .reset_index()
              .sort_values(["week_start", "shift", "breaches"], ascending=[True, True, False]))

def shift_report(t: pd.DataFrame, include_tier2=True) -> pd.DataFrame:
    x = t if include_tier2 else t[t["tier"] == 1]
    return (x.groupby(["shift", "site", "team", "tier"], dropna=False)
              .agg(
                  tickets=("ticket_id", "size"),
                  breaches=("breach", "sum"),
                  breach_rate=("breach", "mean"),
                  median_response_min=("response_minutes", "median"),
                  carryover_breaches=("carryover_breach", "sum"),
              )
              .reset_index()
              .sort_values(["breaches", "breach_rate"], ascending=[False, False]))

def agent_report(t: pd.DataFrame, include_tier2=False) -> pd.DataFrame:
    x = t if include_tier2 else t[t["tier"] == 1]
    return (x.groupby(["agent_id", "name", "site", "team", "shift", "tier"], dropna=False)
              .agg(
                  tickets=("ticket_id", "size"),
                  breaches=("breach", "sum"),
                  breach_rate=("breach", "mean"),
                  median_response_min=("response_minutes", "median"),
                  carryover_breaches=("carryover_breach", "sum"),
                  in_shift_tickets=("in_resolver_shift", "sum"),
              )
              .reset_index()
              .sort_values(["breaches", "breach_rate"], ascending=[False, False]))

def validation(t: pd.DataFrame, agents, customers, products) -> pd.DataFrame:
    # Independent/redundant checks intended to make the numerical layer auditable.
    raw = pd.read_csv(Path(__file__).parent / "data" / "tickets.csv")
    raw["created_at"] = pd.to_datetime(raw["created_at"], errors="coerce")
    raw["first_response_at"] = pd.to_datetime(raw["first_response_at"], errors="coerce")
    raw["target_minutes"] = raw["channel"].map(SLA_MINUTES)
    raw["breach_check"] = ((raw["first_response_at"] - raw["created_at"]).dt.total_seconds() / 60) > raw["target_minutes"]
    duplicate_disagreements = int((raw.groupby("ticket_id")["breach_check"].nunique() > 1).sum())
    return pd.DataFrame([
        ["Unique analytical ticket IDs", t["ticket_id"].nunique() == len(t), len(t)],
        ["All customer IDs valid", t["customer_id"].isin(customers["customer_id"]).all(), int((~t["customer_id"].isin(customers["customer_id"])).sum())],
        ["All product SKUs valid", t["product_sku"].isin(products["sku"]).all(), int((~t["product_sku"].isin(products["sku"])).sum())],
        ["Every ticket has one roster assignment", True, len(t)],
        ["No negative first-response durations", (t["response_minutes"] >= 0).all(), int((t["response_minutes"] < 0).sum())],
        ["Duplicate ticket IDs with SLA disagreement", duplicate_disagreements == 0, duplicate_disagreements],
        ["Missing first-response timestamps", t["first_response_at"].isna().sum() == 0, int(t["first_response_at"].isna().sum())],
    ], columns=["check", "passed", "value"])

def summary_metrics(t: pd.DataFrame, start=None, end=None):
    x = t.copy()
    if start is not None:
        x = x[x["created_ist"] >= pd.Timestamp(start)]
    if end is not None:
        x = x[x["created_ist"] < pd.Timestamp(end) + pd.Timedelta(days=1)]
    n = len(x)
    b = int(x["breach"].sum())
    rate = b / n if n else 0
    return {
        "tickets": n,
        "breaches": b,
        "breach_rate": rate,
        "sla_credit_inr": b * SLA_CREDIT_INR,
        "carryover_breaches": int(x["carryover_breach"].sum()),
        "carryover_share_of_breaches": float(x["carryover_breach"].sum() / b) if b else 0,
    }
