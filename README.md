# Vireo Audio — First-Response SLA Analyzer

A deterministic support SLA reporting tool built with Streamlit. It converts UTC ticket timestamps to IST for roster/shift logic, applies channel-specific first-response targets, deduplicates migration re-imports, and produces weekly agent and shift performance reports. An optional LLM layer generates management-language summaries; **all KPI calculations are fully deterministic**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Business Goal](#business-goal)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Features](#features)
- [SLA Policy](#sla-policy)
- [Data](#data)
- [Outputs](#outputs)
- [Optional AI Summary](#optional-ai-summary)

---

## Overview

Vireo Audio's support team operates across three shifts (Morning, Day, Night) in IST. This tool ingests raw ticket exports (UTC timestamps) alongside effective-dated agent rosters, computes first-response SLA compliance per ticket, and surfaces the breach patterns by shift, agent, channel, and week.

The core insight surfaced by this analysis: **the apparent morning breach spike is largely a queue-coverage artefact, not an agent-performance failure.** 89.1% of recent morning breaches were tickets created outside the resolving agent's staffed shift — carryover from overnight.

---

## Key Findings

| Metric | Value |
|---|---|
| Recent 12-month tickets (Jul 2025–Jun 2026) | 8,934 |
| Total breaches | 2,229 |
| Overall breach rate | **25.0%** |
| SLA credit exposure | **₹7,80,150** |
| Morning share of breaches | 85.5% |
| Morning breaches caused by carryover | **89.1%** |
| Overnight (22:00–05:59 IST) breach rate | **79.1%** |
| Overnight chat breach rate | **100%** |

> **Root cause:** The roster has **zero active Night assignments after 29 Jun 2025**. Overnight tickets (22:00–05:59 IST) pile into the morning queue, inflating morning agent breach counts unfairly.

### Quarterly SLA Credit Exposure

| Quarter | Credit Exposure |
|---|---|
| Q1 2025 | ₹34,650 |
| Q2 2025 | ₹39,200 |
| Q3 2025 | ₹1,67,650 |
| Q4 2025 | ₹2,14,900 |
| Q1 2026 | ₹2,00,550 |
| Q2 2026 | ₹1,97,050 |

The spike begins in **Q3 2025**, coinciding exactly with the removal of the Night shift roster.

---

## Business Goal

| | Value |
|---|---|
| Current breach rate | 25.0% |
| Target breach rate | **15.0%** |
| Estimated fewer breaches/quarter | ~222 |
| Avoided SLA credits/quarter | **~₹77,800** |

The overnight (22:00–05:59) breach rate would need to fall from **79.1% → ~34.6%** (with all other performance held constant) to reach the 15% overall target.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI / Dashboard | [Streamlit](https://streamlit.io/) ≥ 1.40 |
| Data processing | pandas ≥ 2.2, numpy ≥ 1.26 |
| PDF generation | reportlab ≥ 4.0 |
| AI summary (optional) | openai ≥ 1.60 |
| Language | Python 3 |

---

## Project Structure

```
vireo_submission/
│
├── app.py                      # Streamlit dashboard (UI, filters, tabs)
├── core.py                     # Business logic (SLA calc, shift matching, reports)
├── test_core.py                # Unit tests
├── requirements.txt            # Python dependencies
├── run.sh                      # One-shot setup + launch script
│
├── data/                       # Input data pack
│   ├── tickets.csv             # Raw support tickets (UTC timestamps)
│   ├── agents.csv              # Effective-dated agent roster
│   ├── customers.csv           # Customer reference table
│   ├── orders.csv              # Order reference table
│   ├── products.csv            # Product/SKU reference table
│   ├── support-policy.pdf      # Policy document (SLA targets)
│   └── README.txt              # Data pack notes
│
├── outputs/                    # Pre-generated report CSVs
│   ├── weekly_agent_shift_report.csv
│   ├── weekly_tier1_report.csv
│   ├── agent_report_all_tiers.csv
│   ├── agent_report_tier1.csv
│   ├── shift_report.csv
│   ├── shift_attribution_diagnostic.csv
│   ├── monthly_sla_report.csv
│   ├── quarterly_sla_credits.csv
│   ├── overnight_channel_report.csv
│   └── validation_checks.csv
│
├── analysis_findings.md        # Full written analysis
├── validation.md               # Correctness checks
├── scope_decisions.md          # Explicit in/out of scope
├── memo_to_neha.md             # Client-facing management memo
├── memo_to_neha.pdf            # PDF version of memo
├── prompts_used.md             # Prompt evolution log
├── submission-form.md          # Completed submission form
└── screen_recording_script.md  # ≤3 min demo script
```

---

## Getting Started

### Option 1 — One-liner (recommended)

```bash
chmod +x run.sh
./run.sh
```

This creates a virtual environment, installs all dependencies, and launches the app.

### Option 2 — Manual setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Option 3 — Quick run (dependencies already installed)

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## Features

### Dashboard Tabs

| Tab | Contents |
|---|---|
| **Weekly** | Per-agent, per-shift weekly breach report with download |
| **Agents** | Cumulative agent-level performance including carryover diagnostic |
| **Shift / Root Cause** | Shift performance, within-shift vs carryover breakdown, channel view, AI summary |
| **Validation** | 7 automated correctness checks on data integrity |

### Sidebar Filters
- **Date range** — ticket creation date (IST)
- **Tier** — Tier 1 / Tier 2
- **Shift** — Morning / Day / Night
- **Channel** — chat / voice / social / email

### Top-line KPI Bar
```
Eligible tickets | Breaches | Breach rate | SLA credit exposure | Carryover share of breaches
```

### Carryover Diagnostic
Every breach is flagged as **within-shift** or **carryover** (ticket created outside the resolving agent's staffed shift). This prevents queue-coverage failures from being misread as individual agent-performance failures.

---

## SLA Policy

| Channel | First-Response Target | Credit on Miss |
|---|---|---|
| Chat | 15 minutes | ₹350 |
| Voice | 2 hours (120 min) | ₹350 |
| Social | 4 hours (240 min) | ₹350 |
| Email | 8 hours (480 min) | ₹350 |

- SLA elapsed time is computed in **UTC** (raw timestamp difference).
- Shift and roster classification uses **IST** (UTC +05:30).

---

## Data

All required files are already present in `data/`. No additional download or setup needed.

| File | Rows | Notes |
|---|---|---|
| `tickets.csv` | 11,816 raw → 11,200 after dedupe | Includes legacy_fd migration duplicates |
| `agents.csv` | — | Effective-dated roster (from_date / to_date) |
| `customers.csv` | — | Customer reference |
| `orders.csv` | — | Order reference |
| `products.csv` | — | Product/SKU reference |

**Deduplication rule:** When the same `ticket_id` appears in both `helpdesk` and `legacy_fd`, the `helpdesk` copy is kept. All 616 duplicate pairs have identical SLA breach classification.

---

## Outputs

Pre-generated CSV reports are in `outputs/`. The dashboard also offers live **Download** buttons for the weekly and agent reports filtered to your current sidebar selection.

---

## Optional AI Summary

The **"Generate AI summary"** button in the *Shift / Root Cause* tab sends pre-calculated aggregates (not raw data) to OpenAI to produce a plain-English management note.

```bash
export OPENAI_API_KEY="sk-..."
streamlit run app.py
```

If `OPENAI_API_KEY` is not set, a deterministic fallback summary is displayed instead. **The LLM never performs any KPI calculation.**

---

## Running Tests

```bash
python -m pytest test_core.py -v
```

---

## Scope

**In scope:** Weekly first-response SLA reporting · Agent + shift reporting · UTC→IST conversion · Effective-dated roster matching · Migration duplicate handling · Within-shift vs carryover diagnostic · SLA credit exposure · Optional AI summary.

**Out of scope (MVP):** CSAT trends · Refund/replacement economics · Customer segmentation · Product/lot defect analysis · Predictive staffing · Automated agent coaching.
