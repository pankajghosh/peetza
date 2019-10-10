from microcosm.api import binding
from microcosm_postgres.store import Store

from peetza.models.topping_model import Topping


@binding("topping_store")
class ToppingStore(Store):

    def __init__(self, graph):
        super().__init__(self, Topping)
