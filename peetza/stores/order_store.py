from microcosm.api import binding
from microcosm_postgres.store import Store

from peetza.models.order_model import Order


@binding("order_store")
class OrderStore(Store):

    def __init__(self, graph):
        super().__init__(self, Order)
