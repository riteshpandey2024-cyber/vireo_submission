# Vireo Audio — Support SLA Take-Home Submission Form

> **Submission note:** No official `submission-form.md` was included in the supplied assignment pack, so this is a completed submission-ready form based on the assignment brief, supplied data, and required deliverables. Replace any external-link placeholders before submitting.

## 1. Candidate Information

| Field | Response |
|---|---|
| **Name** | Ritesh Pandey |
| **Role / Assignment** | Vireo Audio — Support SLA / AI-Assisted Operations Take-Home |
| **Submission date** | 29 September 2026 |
| **Email** | pandeyriteshp2003@gmail.com |
| **Location** | India |

## 2. Deliverable Summary

### Working AI-assisted tool
**File:** `app.py` + `core.py`

Run locally with:

```bash
./run.sh
```

The tool provides:
- Weekly first-response SLA breach reporting by agent and shift.
- Date, tier, shift, and channel filters.
- Deterministic SLA calculation using the supplied policy.
- UTC → IST conversion for shift and roster logic.
- Effective-dated roster matching.
- Duplicate-ticket handling for migration re-imports.
- Agent, shift, weekly, and overnight-channel views.
- SLA-credit exposure at ₹350 per breach.
- Validation checks and attribution diagnostics.
- Optional LLM-generated management summary; the LLM does not calculate KPIs.

### One-page memo
**File:** `memo_to_neha.pdf`

### Analysis and evidence
- `analysis_findings.md`
- `validation.md`
- `outputs/validation_checks.csv`
- `outputs/weekly_agent_shift_report.csv`
- `outputs/shift_report.csv`
- `outputs/overnight_channel_report.csv`
- `outputs/quarterly_sla_credits.csv`

### Screen recording
**File / link:** `[ADD FINAL SCREEN-RECORDING LINK HERE]`

The planned recording is documented in `screen_recording_script.md` and is designed to stay within the 3-minute limit.

## 3. Business Question

**How can Vireo Audio identify and reduce first-response SLA breaches while reporting performance fairly by agent and shift?**

The requested operational output is a weekly breach report by agent and shift, with enough diagnostic context to distinguish agent-level performance from queue/shift coverage effects.

## 4. Business Goal

### Target
**Reduce first-response SLA breach rate from 25.0% to 15.0% over the next quarter.**

### Baseline
For the selected recent 12-month business-case period (**1 Jul 2025 – 30 Jun 2026**):

- Tickets: **8,934**
- Breaches: **2,229**
- Breach rate: **24.95% (~25.0%)**
- SLA-credit exposure: **₹780,150**

### Expected impact at the recent run-rate
Average recent volume is approximately **2,233.5 tickets per quarter**.

Moving from 24.95% to 15.0% implies approximately:

- **222 fewer breaches per quarter**
- **~₹77,800 lower SLA-credit exposure per quarter** at ₹350 per breach

## 5. Key Finding

The largest apparent concentration is in the **Morning** shift, but the data indicates that this should not be interpreted as evidence that morning agents are inherently slower.

In the recent 12-month period:

- Morning: **1,906 breaches**, or **85.5% of all breaches**.
- Of those morning breaches, **1,698 (89.1%)** were tickets created outside the resolving agent's staffed shift.
- Morning tickets created **within the morning shift** had an **8.3% breach rate**.
- Tickets created during **22:00–05:59 IST** had a **79.1% breach rate (1,579/1,997)**.
- Overnight tickets represented about **70.8% of recent breaches**.
- Overnight chat breached **1,034/1,034 tickets (100%)**.
- The roster contains **no active Night assignment after 29 Jun 2025**.

The practical interpretation is that overnight queue coverage / handoff is a major contributor to the apparent morning breach concentration.

## 6. Recommended Operational Action

1. **Keep the requested weekly agent/shift report, but do not use raw breach count alone for agent coaching.**
2. Add a diagnostic separating tickets created **inside vs. outside the resolving agent's staffed shift**.
3. With headcount frozen, first test **existing-headcount overnight coverage / roster reallocation or a stronger overnight handoff** rather than hiring.
4. Prioritise **overnight chat and social**, followed by email.
5. Track weekly:
   - Overall breach rate.
   - Overnight breach rate.
   - Within-resolver-shift breach rate.
   - Agent/shift breach counts and rates.

A useful operational checkpoint is to bring the **22:00–05:59 IST breach rate toward roughly 35% or below**, assuming other performance remains at the recent baseline.

## 7. Data / Calculation Method

The tool applies the supplied policy deterministically:

- **First response:** first human-agent reply measured from ticket creation.
- **Chat target:** 15 minutes.
- **Voice callback target:** 2 hours.
- **Social target:** 4 hours.
- **Email target:** 8 hours.
- **Breach:** response time greater than the applicable target.
- **SLA credit:** ₹350 per breach.
- Ticket elapsed time is calculated using the supplied UTC timestamps.
- UTC timestamps are converted to IST for shift and roster logic.
- Roster assignment is selected using the ticket's IST creation date and effective roster dates.
- Migration duplicates are deduplicated by `ticket_id`, preferring the helpdesk copy.
- `legacy_fd` CSAT value `0` is treated as no response / missing.
- Agent reporting follows the resolving `agent_id` supplied by the ticket data and README.

## 8. Validation / Correctness Evidence

The deterministic validation suite passed:

| Check | Result |
|---|---:|
| Unique analytical ticket IDs | **11,200** |
| Raw duplicate ticket IDs | **616** |
| Duplicate IDs with SLA classification disagreement | **0** |
| Invalid customer IDs | **0** |
| Invalid product SKUs | **0** |
| Tickets without a first-response timestamp | **0** |
| Negative response durations | **0** |
| Tickets without exactly one effective roster assignment | **0** |
| Independent SLA breach recomputation disagreements | **0** |

The core test also passed with:

`PASS: 11200 unique analytical tickets; 2440 breaches`

## 9. AI / LLM Usage Disclosure

AI was used as an **optional management-language layer**, not as the source of truth for the SLA calculations.

### Deterministic layer
All KPI calculations are performed in Python/pandas in `core.py`.

### LLM layer
The optional LLM receives precomputed aggregates and a small redacted text sample and produces a concise management summary. It is not allowed to calculate or redefine the underlying KPI.

### Fallback
If no `OPENAI_API_KEY` is configured, the tool uses a deterministic summary and still functions without an LLM API call.

### Prompt evolution
Prompt changes and the final prompt approach are documented in `prompts_used.md`.

### Cost
- **Deterministic mode:** ₹0 / $0 API cost.
- **LLM mode:** API cost depends on actual usage, model, and token volume; no API usage is required to run the core SLA analysis.

## 10. Scope Decisions

### Included
- First-response SLA analysis.
- Weekly agent + shift reporting.
- Shift/roster attribution diagnostics.
- SLA-credit exposure.
- Overnight channel analysis.
- Data-quality and correctness validation.
- Optional AI management summary.

### Intentionally excluded from the five-hour MVP
- CSAT trend analysis.
- Refund/replacement economics.
- Customer segmentation.
- Product/lot defect analysis.
- Predictive staffing.
- Automated agent coaching.
- Full free-text root-cause classification.

These were excluded because the stated request is a weekly SLA report and the available data already exposes a material queue-coverage issue that can be acted on directly.

## 11. Files Included

```text
vireo_submission/
├── app.py
├── core.py
├── requirements.txt
├── run.sh
├── test_core.py
├── submission-form.md
├── memo_to_neha.md
├── memo_to_neha.pdf
├── analysis_findings.md
├── validation.md
├── prompts_used.md
├── screen_recording_script.md
├── scope_decisions.md
├── README_SUBMISSION.md
├── data/
└── outputs/
```

## 12. Final Submission Links

- **Submission package:** `vireo_audio_sla_submission.zip`
- **Screen recording:** `[ADD FINAL SCREEN-RECORDING LINK HERE]`
- **Hosted tool URL, if applicable:** `[OPTIONAL — ADD URL HERE]`

## 13. Short Submission Statement

> I built a deterministic SLA reporting tool that converts UTC ticket timestamps to IST for shift logic, applies the supplied channel targets, handles migration duplicates and effective-dated roster assignments, and reports weekly breaches by agent and shift. The analysis shows that the apparent morning concentration is largely driven by overnight queue carryover: 89.1% of recent morning breaches were created outside the resolving agent's staffed shift. The proposed operational goal is to reduce the overall breach rate from ~25% to 15% over the next quarter, using existing-headcount overnight coverage and handoff improvements as the first experiment. An optional LLM layer is used only for management-language summaries; all KPI calculations remain deterministic and validated.
