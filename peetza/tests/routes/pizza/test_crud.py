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
from peetza.models.pizza_model import Pizza, PizzaSize, PizzaType


class TestPizzaRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.new_pizza = Pizza(
            id=new_object_id(),
            pizza_size=PizzaSize.SMALL.name,
            pizza_type=PizzaType.HANDTOSSED.name,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.new_pizza.create()

        uri = "/api/v1/pizza"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                items=contains(
                    has_entries(
                        pizza_size=self.new_pizza.pizza_size,
                        pizza_type=self.new_pizza.pizza_type,
                    ),
                ),
            ),
        )

    def test_replace_with_new(self):
        uri = f"/api/v1/pizza/{self.new_pizza.id}"

        response = self.client.put(
            uri,
            json=dict(
                pizza_size=self.new_pizza.pizza_size,
                pizza_type=self.new_pizza.pizza_type,
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        assert_that(
            response.json,
            has_entries(
                id=str(self.new_pizza.id),
                pizza_size=self.new_pizza.pizza_size,
                pizza_type=self.new_pizza.pizza_type,
            ),
        )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.new_pizza.create()

        uri = f"/api/v1/pizza/{self.new_pizza.id}"

        response = self.client.get(uri)

        assert_that(
            response.json,
            has_entries(
                id=str(self.new_pizza.id),
                pizza_size=self.new_pizza.pizza_size,
                pizza_type=self.new_pizza.pizza_type,
            ),
        )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.new_pizza.create()

        uri = f"/api/v1/pizza/{self.new_pizza.id}"

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
