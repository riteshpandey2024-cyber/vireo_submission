# Vireo Audio — Support SLA submission pack

## Run
```bash
./run.sh
```
Or:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app expects the supplied data files in `data/`.

## What the tool does
- Converts UTC ticket timestamps to IST for roster/shift logic.
- Applies policy first-response targets deterministically.
- Deduplicates migration re-imports by ticket_id.
- Matches the effective roster assignment.
- Produces weekly agent/shift reports.
- Separates within-shift performance from queue carryover.
- Shows SLA-credit exposure.
- Offers an optional LLM management summary; the LLM does not calculate KPIs.

## Key business finding
The recent 12-month baseline is 25.0% first-response breach rate (2,229 / 8,934). Morning contains 85.5% of breaches, but 89.1% of morning breaches are tickets created outside the resolving agent's staffed shift. The roster has no active Night assignment after 29 Jun 2025. Overnight 22:00–05:59 tickets have a 79.1% breach rate.

## Business goal
Reduce the recent 12-month breach rate from 25.0% to 15.0%, approximately 222 fewer breaches per quarter and ~₹77,800/quarter in avoided SLA credits at the recent ticket run-rate.

## Files
- `app.py`, `core.py`: working tool
- `data/`: supplied data pack
- `outputs/`: generated reports
- `memo_to_neha.pdf`: one-page client memo
- `analysis_findings.md`: analysis
- `validation.md`: correctness checks
- `prompts_used.md`: prompt evolution
- `screen_recording_script.md`: ≤3 minute recording plan
- `scope_decisions.md`: explicit scope decisions

`submission-form.md` was not included because it was not supplied in the uploaded pack. Fill the actual form from the findings above when it is provided.
