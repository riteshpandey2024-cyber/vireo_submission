# Validation / correctness

## Numerical validation
The KPI layer is deterministic. It was checked with:
1. **11,200 unique analytical tickets** after migration deduplication.
2. **0 negative** first-response durations.
3. **0 duplicate-ticket SLA disagreements** between the helpdesk and legacy copies.
4. **100% customer IDs** present in `customers.csv`.
5. **100% product SKUs** present in `products.csv`.
6. **100% of analytical tickets** matched exactly one effective roster assignment using the ticket's IST creation date.
7. An independent recomputation of `breach = elapsed(created_at → first_response_at) > channel target` produced **0 disagreements** with the production calculation.

## Known data caveats
- 616 ticket IDs appear twice, once under each source system. The duplicate copies are migration re-imports. The tool keeps one analytical row per ticket and prefers the current helpdesk copy. SLA breach classification is identical across the duplicate copies.
- Legacy `csat_score=0` is treated as no response, per the pack/policy.
- 4,620 tickets have no `order_id`; all have a customer+SKU fallback match, but 382 customer+SKU pairs map to multiple historical orders. Order-level attribution is therefore intentionally not used in the SLA KPI.
- 6 tickets contain both a refund and replacement flag, a policy exception. Refund/replacement analysis is outside the SLA MVP.
- Tier 2 is displayed separately because policy says Tier 2 should not be compared with Tier 1 on volume metrics.
