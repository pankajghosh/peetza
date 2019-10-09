"""
Example persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from peetza.models.pizza_model import Pizza


@binding("pizza_store")
class PizzaStore(Store):

    def __init__(self, graph):
        super().__init__(self, Pizza)


