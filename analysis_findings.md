# Vireo Audio — Analysis findings

## 1. Core SLA definition
Policy v3.2 defines first response as the first human-agent reply measured from ticket creation. Targets: chat 15 minutes, voice callback 2 hours, social 4 hours, email 8 hours. Every miss issues a ₹350 store credit.

The export is UTC; the policy's shift definitions are IST. Therefore:
- elapsed SLA = UTC timestamp difference;
- shift/roster classification = timestamps converted to IST.

## 2. Data preparation
- Raw tickets: 11,816 rows.
- Unique analytical tickets after migration dedupe: 11,200.
- Duplicate ticket IDs: 616 IDs, each represented once in helpdesk and once in legacy_fd.
- Duplicate copies have identical SLA breach classification.
- 0 negative response durations.
- All 11,200 customer IDs and product SKUs join to reference tables.
- Every ticket maps to exactly one effective roster assignment on its IST creation date.

## 3. Baseline
All 18 months:
- 11,200 tickets
- 2,440 breaches
- 21.8% breach rate
- ₹854,000 credit exposure

The earlier period is structurally different from the recent period. Jul 2025–Jun 2026 is therefore used for the business case:
- 8,934 tickets
- 2,229 breaches
- 25.0% breach rate
- ₹780,150 credit exposure

## 4. The apparent morning problem is mostly queue carryover
Recent 12 months:
- Morning: 5,187 tickets, 1,906 breaches, 36.7% breach rate.
- 1,698 of those 1,906 morning breaches (89.1%) were tickets created outside the resolving agent's staffed shift.
- Morning tickets created within the morning shift: 8.3% breach rate.

This means raw morning breach counts are not a fair standalone agent-performance measure.

## 5. Overnight queue coverage is the strongest structural signal
Recent 12 months, 22:00–05:59 IST:
- 1,997 tickets
- 1,579 breaches
- 79.1% breach rate
- ₹552,650 credit exposure

Overnight chat:
- 1,034 tickets
- 1,034 breaches
- 100.0% breach rate
- ₹361,900 credit exposure

The roster has zero active Night assignments after 29 Jun 2025. The policy says overnight chat coverage is provided by the Indore Night shift and that out-of-hours queue coverage moves to the next shift. The observed morning concentration is consistent with this carryover mechanism.

## 6. Finance signal
Quarterly SLA-credit exposure:
- Q1 2025: ₹34,650
- Q2 2025: ₹39,200
- Q3 2025: ₹167,650
- Q4 2025: ₹214,900
- Q1 2026: ₹200,550
- Q2 2026: ₹197,050

The change begins in Jul 2025, which is also when the roster no longer has an active Night assignment.

## 7. Business goal
Target: 15.0% recent-period breach rate.
At 2,233.5 average tickets/quarter, moving from 25.0% to 15.0% means about 222 fewer breaches per quarter, worth about ₹77,800 per quarter in avoided SLA credits.

If all non-overnight performance stayed at its recent baseline, the 22:00–05:59 breach rate would need to fall to roughly 34.6% to reach a 15% overall rate.

## 8. Agent-level fairness diagnostic
Several high raw-breach morning agents have low within-shift breach rates but high carryover rates. Example, last 12 months:
- A3037 Rahul Sen: 166 total breaches / 34.6%; within-shift 8.2%, carryover 62.1%.
- A3028 Krishna Kaur: 161 / 36.6%; within-shift 7.6%, carryover 66.7%.
- A3031 Om Malhotra: 152 / 34.5%; within-shift 8.3%, carryover 60.1%.

This is why the tool displays carryover separately instead of treating raw breach count as direct agent fault.

## 9. Intentional scope exclusions
CSAT, refunds/replacements, product/lot analysis, and customer segmentation are not used in the core KPI because they do not answer the stated SLA question. They can be added later if a follow-up investigation requires them.
