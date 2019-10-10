"""
Example controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from peetza.models.customer_event_model import CustomerEvent


@binding("customer_event_controller")
class CustomerEventController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.customer_event_store)

        self.ns = Namespace(
            subject=CustomerEvent,
            version="v1",
        )
