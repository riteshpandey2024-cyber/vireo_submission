
import os
from pathlib import Path
import pandas as pd
import streamlit as st

from core import load_data, prepare_tickets, weekly_report, shift_report, agent_report, validation, summary_metrics, SLA_CREDIT_INR

st.set_page_config(page_title="Vireo Audio — SLA Analyzer", layout="wide")
DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def get_data():
    raw = load_data(DATA_DIR)
    prepared = prepare_tickets(raw[0], raw[1])
    return prepared, raw

t, raw = get_data()
tickets_raw, agents, customers, orders, products = raw

st.title("Vireo Audio — First-Response SLA Analyzer")
st.caption("Deterministic KPI layer + optional AI management summary. All ticket timestamps are treated as UTC; shift logic is evaluated in IST.")

with st.sidebar:
    st.header("Filters")
    min_date = t["created_ist"].min().date()
    max_date = t["created_ist"].max().date()
    default_start = max(min_date, (t["created_ist"].max() - pd.DateOffset(months=12)).date())
    date_range = st.date_input("Ticket creation date", value=(default_start, max_date), min_value=min_date, max_value=max_date)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
    else:
        start, end = min_date, max_date

    tiers = st.multiselect("Tier", sorted(t["tier"].unique()), default=sorted(t["tier"].unique()))
    shifts = st.multiselect("Shift", sorted(t["shift"].unique()), default=sorted(t["shift"].unique()))
    channels = st.multiselect("Channel", sorted(t["channel"].unique()), default=sorted(t["channel"].unique()))

f = t[
    (t["created_ist"].dt.date >= start) &
    (t["created_ist"].dt.date <= end) &
    (t["tier"].isin(tiers)) &
    (t["shift"].isin(shifts)) &
    (t["channel"].isin(channels))
].copy()

m = summary_metrics(f)
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Eligible tickets", f"{m['tickets']:,}")
c2.metric("Breaches", f"{m['breaches']:,}")
c3.metric("Breach rate", f"{m['breach_rate']:.1%}")
c4.metric("SLA credit exposure", f"₹{m['sla_credit_inr']:,.0f}")
c5.metric("Carryover share of breaches", f"{m['carryover_share_of_breaches']:.1%}")

st.info(
    "Diagnostic: 'carryover' means the ticket was created outside the resolving agent's staffed shift. "
    "It is still a real SLA breach; the flag prevents the report from treating queue-coverage breaches as purely agent-performance failures."
)

tab1, tab2, tab3, tab4 = st.tabs(["Weekly", "Agents", "Shift / Root Cause", "Validation"])

with tab1:
    st.subheader("Weekly agent + shift report")
    wr = weekly_report(f, include_tier2=True)
    st.dataframe(wr, use_container_width=True, hide_index=True)
    st.download_button("Download weekly report CSV", wr.to_csv(index=False), "vireo_weekly_sla_report.csv", "text/csv")

with tab2:
    st.subheader("Agent view")
    st.caption("Tier 2 is shown but should not be compared with Tier 1 on volume metrics under policy.")
    ar = agent_report(f, include_tier2=True)
    st.dataframe(ar, use_container_width=True, hide_index=True)
    st.download_button("Download agent report CSV", ar.to_csv(index=False), "vireo_agent_sla_report.csv", "text/csv")

with tab3:
    sr = shift_report(f, include_tier2=True)
    st.subheader("Shift performance")
    st.dataframe(sr, use_container_width=True, hide_index=True)

    st.subheader("Within-shift vs carryover")
    diag = (
        f.groupby(["shift", "in_resolver_shift"])
         .agg(tickets=("ticket_id","size"), breaches=("breach","sum"), breach_rate=("breach","mean"))
         .reset_index()
    )
    diag["classification"] = diag["in_resolver_shift"].map({True:"Created within resolver shift", False:"Created outside resolver shift"})
    st.dataframe(diag[["shift","classification","tickets","breaches","breach_rate"]], use_container_width=True, hide_index=True)

    st.subheader("Channel")
    ch = f.groupby("channel").agg(tickets=("ticket_id","size"), breaches=("breach","sum"), breach_rate=("breach","mean"), median_response_min=("response_minutes","median")).reset_index()
    st.dataframe(ch, use_container_width=True, hide_index=True)

    st.subheader("AI management summary")
    st.caption("The LLM never calculates the KPI. It receives already-calculated aggregates and a small redacted text sample only.")
    if st.button("Generate AI summary"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.warning("OPENAI_API_KEY is not set. Use the deterministic summary below or set the key and rerun.")
            morning = f[f["shift"]=="Morning"]
            overnight = f[(f["created_ist"].dt.hour >= 22) | (f["created_ist"].dt.hour < 6)]
            st.write(
                f"Across {len(f):,} tickets, {int(f.breach.sum()):,} breached first-response SLA "
                f"({f.breach.mean():.1%}). Morning accounts for {int(morning.breach.sum()):,} breaches. "
                f"{int(f.carryover_breach.sum()):,} breaches were on tickets created outside the resolving agent's staffed shift. "
                f"Overnight (22:00–05:59 IST) is the main queue-coverage risk."
            )
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                x = f.copy()
                sample = x[x["breach"]].sample(min(20, len(x[x["breach"]])), random_state=7)[
                    ["channel","category","priority","customer_message","agent_notes"]
                ].fillna("").copy()
                # Redact common customer/order identifiers before sending text to the model.
                sample["customer_message"] = sample["customer_message"].str.replace(r"\bC\d{5,}\b", "[CUSTOMER_ID]", regex=True).str.replace(r"\bVR\d{6,}\b", "[ORDER_ID]", regex=True)
                sample["agent_notes"] = sample["agent_notes"].str.replace(r"\bC\d{5,}\b", "[CUSTOMER_ID]", regex=True).str.replace(r"\bVR\d{6,}\b", "[ORDER_ID]", regex=True)
                payload = {
                    "period": [str(start), str(end)],
                    "tickets": len(f),
                    "breaches": int(f.breach.sum()),
                    "breach_rate": round(float(f.breach.mean()),4),
                    "sla_credit_inr": int(f.breach.sum()*SLA_CREDIT_INR),
                    "carryover_breaches": int(f.carryover_breach.sum()),
                    "shift_table": sr.to_dict("records"),
                    "sample_breach_text": sample.to_dict("records"),
                }
                prompt = """You are writing a concise support-operations note. Use only the supplied calculated metrics and text sample.
Do not recalculate KPIs, rank agents as 'bad', or blame agents for carryover breaches. Separate structural queue-coverage issues
from within-shift performance. State uncertainty where the sample is small. Return 5 bullets: what happened, where, likely operational
mechanism, what to investigate next, and what not to conclude."""
                resp = client.responses.create(
                    model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),
                    input=prompt + "\n\nDATA:\n" + str(payload)
                )
                st.write(resp.output_text)
            except Exception as e:
                st.error(f"AI call failed: {e}")

with tab4:
    st.subheader("Automated validation")
    v = validation(t, agents, customers, products)
    st.dataframe(v, use_container_width=True, hide_index=True)
    st.caption("Numerical SLA classification is deterministic; the LLM is not used for the KPI calculation.")
