"""
Example CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from peetza.app import create_app
from peetza.models.order_model import Order


class TestOrderRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.new_order = Order(
            id=new_object_id(),
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_create_and_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.new_order.create()

        uri = f"/api/v1/order/{self.new_order.id}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.new_order.id),
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.new_order.create()

        uri = f"/api/v1/order/{self.new_order.id}"

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
