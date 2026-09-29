VIREO AUDIO — SUPPORT DATA PACK
================================

tickets.csv          Support tickets, 1 Jan 2025 – 30 Jun 2026. All timestamps in this export are UTC.
agents.csv            Roster. One row per assignment (agent_id, name, site, team, shift, tier, from_date, to_date).
customers.csv         Customers reference table.
orders.csv            Orders reference table.
products.csv          Products reference table.
support-policy.pdf    Vireo support operating policy v3.2.
email-thread.txt      Stakeholder context already exchanged.

Important data rules used by the tool:
- Ticket timestamps are UTC; convert to IST before applying roster/shift logic.
- First-response SLA is elapsed time from created_at to first_response_at.
- Policy targets: chat 15m, voice callback 2h, social 4h, email 8h.
- Breach = first response later than the channel target.
- Breaches are reported against the resolving agent.
- Duplicate ticket IDs across helpdesk and legacy_fd are migration re-imports; the tool keeps one row per ticket_id, preferring helpdesk where available. Duplicate copies have identical SLA breach classification.
- Legacy CSAT 0 means no response and is normalized to missing for analysis.
- Roster matching uses the agent's assignment effective on the ticket's IST creation date.
