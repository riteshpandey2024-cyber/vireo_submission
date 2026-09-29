# Vireo Audio — First-response SLA breach memo
**To:** Neha Kulkarni, Support Operations Manager  
**Period used for the business case:** 1 Jul 2025–30 Jun 2026  
**Purpose:** weekly breach reporting by agent and shift, with a fair attribution diagnostic.

## Business goal
Reduce first-response SLA breaches from **25.0% to 15.0%** over the next quarter. At the recent 12-month ticket volume, that is about **222 fewer breaches per quarter**, or approximately **₹77,800 per quarter** in avoided ₹350 SLA credits.

## What the data says
- The recent 12-month baseline is **2,229 breaches out of 8,934 tickets (25.0%)**, representing **₹780,150** in SLA-credit exposure.
- **Morning carries 1,906 breaches (85.5% of all breaches)** and a 36.7% breach rate. However, this should not be read as morning-agent performance: **1,698 of those morning breaches (89.1%) were tickets created outside the resolving agent's staffed shift**. For tickets created within the morning shift, the breach rate is only **8.3%**.
- The main structural issue is overnight queue carryover. Tickets created **22:00–05:59 IST** have a **79.1% breach rate (1,579/1,997)** and account for about **₹552,650** of credit exposure in the last 12 months. Overnight chat is the clearest problem: **1,034/1,034** overnight chat tickets breached.
- The roster shows **no active Night assignment after 29 Jun 2025**. The policy says overnight chat coverage is provided by the Indore Night shift and that out-of-hours queue coverage moves to the next shift. This makes the apparent morning breach concentration consistent with queue carryover rather than evidence that morning agents are inherently slow.
- SLA-credit exposure rose from **₹39,200 in Q2 2025 to ₹167,650 in Q3 2025**, then remained around ₹197k–₹215k per quarter through Q2 2026. This is consistent with the finance concern that the credit line changed materially after last summer.

## Recommended action
1. **Do not use raw breach count as a morning-agent coaching metric.** Keep the requested weekly agent/shift report, but show a separate “created outside resolver shift” flag.
2. **Use existing headcount to restore explicit overnight queue coverage or redesign the overnight handoff.** Headcount is frozen, so the first experiment should be a roster/shift reallocation rather than hiring.
3. Prioritise **overnight chat and social**, then email. These channels have tight targets and show the strongest overnight breach concentration.
4. Track three weekly measures: overall breach rate, overnight breach rate, and within-resolver-shift breach rate. A practical checkpoint for the 15% overall goal is to bring the 22:00–05:59 breach rate down to roughly **35% or below**, assuming other performance stays at the recent baseline.

## Measurement / controls
The tool converts UTC timestamps to IST for shift logic, applies the policy channel targets deterministically, deduplicates migration re-imports by `ticket_id` (preferring the helpdesk copy), and validates roster/customer/product joins. The LLM is used only for management-language summaries; it does not calculate SLA KPIs.

**Scope intentionally left out:** CSAT, refunds/replacements, and detailed customer segmentation are available in the pack but are not necessary to answer the stated SLA question. They can be investigated later if they materially explain the breach pattern.
