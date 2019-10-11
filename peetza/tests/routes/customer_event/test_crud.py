"""
Example CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""

from hamcrest import (
    assert_that,
    contains,
    equal_to,
    has_entries,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from peetza.app import create_app
from peetza.models.customer_event_model import CustomerStartedOrder
from peetza.models.order_model import Order
from peetza.models.pizza_model import PizzaSize


class TestCustomerEventRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)
        with SessionContext(self.graph), transaction():
            self.new_order = Order().create()

        self.customer_event = CustomerStartedOrder(id=new_object_id(), order_id=self.new_order.id)

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.customer_event.create()

        uri = "/api/v1/customer_event"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        order_id=str(self.new_order.id),
                        event_type=str(self.customer_event.event_type),
                    ),
                ),
            ),
        )

    def test_replace_with_new(self):
        uri = f"/api/v1/customer_event/{self.customer_event.id}"

        response = self.client.put(
            uri,
            json=dict(
                event_type=str(self.customer_event.event_type),
                order_id=self.new_order.id,
                pizza_size=PizzaSize.SMALL.name,
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.customer_event.id),
                order_id=str(self.new_order.id),
                pizza_size=str(PizzaSize.SMALL.name),
                event_type=str(self.customer_event.event_type),
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.customer_event.create()

        uri = f"/api/v1/customer_event/{self.customer_event.id}"

        response = self.client.get(uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.customer_event.id),
                order_id=str(self.new_order.id),
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.customer_event.create()

        uri = f"/api/v1/customer_event/{self.customer_event.id}"

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
