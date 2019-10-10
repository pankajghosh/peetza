"""
Example persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
)
from hamcrest.core.core import raises
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.errors import ModelNotFoundError

from peetza.app import create_app
from peetza.models.order_model import Order
from peetza.models.pizza_model import PizzaSize, PizzaType


class TestOrderStore:

    def setup(self):
        self.graph = create_app(testing=True)
        self.pizza_store = self.graph.pizza_store
        self.order_store = self.graph.order_store

        self.pizza_type = PizzaType.HANDTOSSED.name
        self.pizza_size = PizzaSize.SMALL.name

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        new_order = Order()

        with transaction():
            self.order_store.create(new_order)

        retreived_order = self.order_store.retrieve(new_order.id)
        assert_that(retreived_order, is_(equal_to(new_order)))

    def test_delete_order(self):
        new_order = Order().create()

        retreived_order = self.order_store.retrieve(new_order.id)
        assert_that(retreived_order, is_(equal_to(new_order)))

        new_order.delete()
        assert_that(
            calling(self.order_store.retrieve).with_args(identifier=new_order.id),
            raises(ModelNotFoundError),
        )
