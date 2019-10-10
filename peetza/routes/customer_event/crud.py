"""
Example CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from peetza.resources.customer_event_resources import (
    CustomerEventSchema,
    NewCustomerEventSchema,
    SearchCustomerEventSchema,
)


@binding("customer_event_routes")
def configure_customer_event_routes(graph):
    controller = graph.customer_event_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewCustomerEventSchema(),
            response_schema=CustomerEventSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Replace: EndpointDefinition(
            func=transactional(controller.replace),
            request_schema=NewCustomerEventSchema(),
            response_schema=CustomerEventSchema(),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=CustomerEventSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchCustomerEventSchema(),
            response_schema=CustomerEventSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
