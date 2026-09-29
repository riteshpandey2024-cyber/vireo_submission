
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from core import load_data, prepare_tickets

DATA = Path(__file__).parent / "data"
tickets, agents, customers, orders, products = load_data(DATA)
t = prepare_tickets(tickets, agents)

assert len(t) == t.ticket_id.nunique()
assert t.customer_id.isin(customers.customer_id).all()
assert t.product_sku.isin(products.sku).all()
assert (t.response_minutes >= 0).all()
assert t.first_response_at.notna().all()
print("PASS:", len(t), "unique analytical tickets;", int(t.breach.sum()), "breaches")
