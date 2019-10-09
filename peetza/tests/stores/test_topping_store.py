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
from microcosm_postgres.identifiers import new_object_id

from peetza.app import create_app
from peetza.models.pizza_model import Pizza, PizzaSize, PizzaType
from peetza.models.topping_model import ToppingType, Topping


class TestToppingStore:

    def setup(self):
        self.graph = create_app(testing=True)
        self.topping_store = self.graph.topping_store
        self.pizza_store = self.graph.pizza_store

        self.pizza_type = PizzaType.HANDTOSSED.name
        self.pizza_size = PizzaSize.SMALL.name

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

        self.new_pizza = Pizza(
            pizza_size=self.pizza_size,
            pizza_type=self.pizza_type,
        ).create()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        new_topping = Topping(
            pizza_id = self.new_pizza.id,
            topping_type = ToppingType.CHICKEN,
        )

        with transaction():
            self.topping_store.create(new_topping)

        retrieved_topping = self.topping_store.retrieve(new_topping.id)
        assert_that(retrieved_topping, is_(equal_to(new_topping)))

    def test_search_toppings(self):
        Topping(
            pizza_id = self.new_pizza.id,
            topping_type = ToppingType.CHICKEN,
        ).create()
        Topping(
            pizza_id = self.new_pizza.id,
            topping_type = ToppingType.ONIONS,
        ).create()

        assert_that(self.topping_store.search(pizza_id=self.new_pizza.id), has_length(2))

    def test_delete_topping(self):
        assert_that(self.topping_store.search(pizza_id=self.new_pizza.id), has_length(0))
        new_topping = Topping(
            pizza_id = self.new_pizza.id,
            topping_type = ToppingType.CHICKEN,
        ).create()

        assert_that(self.topping_store.search(pizza_id=self.new_pizza.id), has_length(1))

        new_topping.delete()
        assert_that(self.topping_store.search(pizza_id=self.new_pizza.id), has_length(0))
