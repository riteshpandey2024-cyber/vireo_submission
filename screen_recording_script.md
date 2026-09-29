# 3-minute screen-recording script

## 0:00–0:25 — Start with the result
“I'm going to show the working SLA analyzer, then the prompt I used, what changed, and what I deliberately left out.”

Open the app and show the KPI cards:
- 8,934 tickets in the recent 12-month view
- 2,229 breaches
- 25.0% breach rate
- ₹780,150 SLA-credit exposure
- carryover share

## 0:25–1:05 — Show the weekly report
Open Weekly.
Say:
“Neha asked for weekly reporting by agent and shift. The numerical layer is deterministic. It converts the API's UTC timestamps to IST for shift logic, applies the policy channel targets, and reports breaches against the resolving agent.”

Open Agents.
Show that the report includes ticket volume, breach count/rate, median response, and carryover breaches.

## 1:05–1:50 — Show the key finding
Open Shift / Root Cause.
Say:
“The important change was adding the within-shift versus carryover split. Morning looks responsible for 85.5% of recent breaches, but 89.1% of morning breaches were tickets created outside the morning shift. Within the morning shift, the breach rate is only 8.3%.”

Show the overnight table:
“22:00–05:59 has a 79.1% breach rate. The roster has no active Night assignment after June 29, while policy says overnight coverage is provided by the Indore Night shift.”

## 1:50–2:25 — Prompt evolution
Open prompts_used.md.
Say:
“V1 asked the model for a summary. V2 added attribution awareness. The final prompt explicitly tells the model not to recalculate KPIs or blame agents for carryover breaches. The LLM receives aggregates and a small redacted text sample; it never calculates the SLA metric.”

## 2:25–2:45 — What I discarded
“Given the five-hour cap, I left CSAT, refunds, replacements, and detailed customer segmentation out of the MVP. I also discarded LLM-based KPI calculation and raw-breach agent ranking because they add risk without answering the client's question.”

## 2:45–3:00 — Close
“The business goal is to reduce the recent 12-month breach rate from 25.0% to 15.0%, which is about 222 fewer breaches per quarter and roughly ₹77,800 per quarter in avoided SLA credits. The first operational experiment is existing-headcount overnight coverage or a better overnight handoff, not hiring.”
