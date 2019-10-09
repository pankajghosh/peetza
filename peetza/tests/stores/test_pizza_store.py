"""
Example persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction

from peetza.app import create_app
from peetza.models.pizza_model import Pizza, PizzaSize, PizzaType


class TestPizzaStore:

    def setup(self):
        self.graph = create_app(testing=True)
        self.pizza_store = self.graph.pizza_store

        self.pizza_type = PizzaType.HANDTOSSED.name
        self.pizza_size = PizzaSize.SMALL.name

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        new_pizza = Pizza(
            pizza_size=self.pizza_size,
            pizza_type=self.pizza_type,
        )

        with transaction():
            self.pizza_store.create(new_pizza)

        retrieved_pizza = self.pizza_store.retrieve(new_pizza.id)
        assert_that(retrieved_pizza, is_(equal_to(new_pizza)))

    def test_create_multiple(self):
        with transaction():
            self.pizza_store.create(Pizza(
                pizza_size=self.pizza_size,
                pizza_type=self.pizza_type, ))

            self.pizza_store.create(Pizza(
                pizza_size=self.pizza_size,
                pizza_type=self.pizza_type, ))

        assert_that(self.pizza_store.search(), has_length(2))
