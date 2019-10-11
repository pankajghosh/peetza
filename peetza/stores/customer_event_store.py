from microcosm.api import binding
from microcosm_postgres.store import Store

from peetza.models.customer_event_model import CustomerEvent


@binding("customer_event_store")
class CustomerEventStore(Store):

    def __init__(self, graph):
        super().__init__(self, CustomerEvent)
