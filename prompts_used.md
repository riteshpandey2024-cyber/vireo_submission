# Prompt versions used / proposed for the recording

## V1 — initial summary prompt
“Summarise the weekly first-response SLA results by agent and shift. Mention the largest breach concentrations and the main operational pattern.”

### What changed
This was too easy for the model to over-attribute raw breaches to individual agents.

## V2 — attribution-aware prompt
“You are a support-operations analyst. Summarise weekly first-response SLA results using only the supplied calculated metrics. Distinguish tickets created within the resolving agent's shift from tickets created outside that shift. Do not infer that a raw breach count means an agent caused the breach.”

### What changed
Added the queue-carryover diagnostic and an explicit no-blame constraint.

## Final prompt
“You are writing a concise support-operations note. Use only the supplied calculated metrics and a small redacted text sample. Do not recalculate KPIs, rank agents as ‘bad’, or blame agents for carryover breaches. Separate structural queue-coverage issues from within-shift performance. State uncertainty where the sample is small. Return 5 bullets: what happened, where, likely operational mechanism, what to investigate next, and what not to conclude.”

### What was discarded
- Asking the LLM to calculate breach percentages.
- Sending the full ticket table to the model.
- Ranking agents using only raw breach count.
- Using CSAT/refund fields to create a broader scorecard in the first version.

## AI cost disclosure
The deterministic tool runs at zero model/API cost. The optional AI summary uses an OpenAI API key supplied by the operator; actual cost depends on the model and number of calls. No API call is required for the numerical KPI layer.
