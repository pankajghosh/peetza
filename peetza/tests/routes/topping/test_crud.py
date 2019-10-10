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
    has_length,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.identifiers import new_object_id
from microcosm_postgres.operations import recreate_all

from peetza.app import create_app
from peetza.models.order_model import Order
from peetza.models.pizza_model import Pizza, PizzaSize, PizzaType
from peetza.models.topping_model import Topping, ToppingType


class TestToppingRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        with SessionContext(self.graph), transaction():
            self.new_order = Order().create()

            self.new_pizza = Pizza(
                id=new_object_id(),
                order_id=self.new_order.id,
                pizza_size=PizzaSize.SMALL.name,
                pizza_type=PizzaType.HANDTOSSED.name,
            ).create()

        self.first_topping = Topping(
            id=new_object_id(),
            pizza_id=self.new_pizza.id,
            topping_type=ToppingType.ONIONS,
        )

        self.second_topping = Topping(
            id=new_object_id(),
            pizza_id=self.new_pizza.id,
            topping_type=ToppingType.CHICKEN,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.first_topping.create()

        uri = "/api/v1/topping"

        response = self.client.get(
            uri,
            query_string=dict(
                pizza_id=str(self.new_pizza.id),
            )
        )

        assert_that(response.status_code, is_(equal_to(200)))
        data = response.json
        assert_that(data["items"], contains(
            has_entries(
                pizza_id=str(self.new_pizza.id),
                topping_type=self.first_topping.topping_type.name,
            ),
        ))

    def test_replace_with_new(self):
        uri = f"/api/v1/topping/{self.first_topping.id}"

        response = self.client.put(
            uri,
            json=dict(
                pizza_id=str(self.new_pizza.id),
                topping_type=ToppingType.BLACK_OLIVES.name,
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        data = response.json
        assert_that(data, has_entries(
            pizza_id=str(self.new_pizza.id),
            topping_type=ToppingType.BLACK_OLIVES.name,
        ),
                    )

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.first_topping.create()

        uri = f"/api/v1/topping/{self.first_topping.id}"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = response.json
        assert_that(data, has_entries(
            pizza_id=str(self.new_pizza.id),
            topping_type=self.first_topping.topping_type.name,
        ),
                    )

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.first_topping.create()

        uri = f"/api/v1/topping/{self.first_topping.id}"

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))

    def test_multiple_toppings(self):
        with SessionContext(self.graph), transaction():
            self.first_topping.create()
            self.second_topping.create()

        uri = "/api/v1/topping"

        response = self.client.get(
            uri,
            query_string=dict(
                pizza_id=str(self.new_pizza.id),
            )
        )

        assert_that(response.status_code, is_(equal_to(200)))
        data = response.json
        assert_that(data["items"], has_length(2))
