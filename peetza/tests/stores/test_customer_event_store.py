"""
Example persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
    calling, raises)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.errors import ModelNotFoundError

from peetza.app import create_app
from peetza.models.customer_event_model import CustomerStartedOrder, CustomerAddedTopping
from peetza.models.order_model import Order
from peetza.models.topping_model import ToppingType


class TestOrderStore:

    def setup(self):
        self.graph = create_app(testing=True)
        self.customer_event_store = self.graph.customer_event_store
        self.pizza_store = self.graph.pizza_store
        self.order_store = self.graph.order_store
        self.topping_store = self.graph.topping_store

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create_customer_started_order(self):
        new_order = Order()

        with transaction():
            new_order = self.order_store.create(new_order)
            customer_event = self.customer_event_store.create(CustomerStartedOrder(order_id=new_order.id))

        retreived_customer_event = self.customer_event_store.retrieve(customer_event.id)
        assert_that(retreived_customer_event, is_(equal_to(customer_event)))

    def test_create_customer_added_topping(self):
        with transaction():
            new_order = self.order_store.create(Order())
            customer_started_order = self.customer_event_store.create(CustomerStartedOrder(order_id=new_order.id))
            customer_added_topping = self.customer_event_store.create(
                CustomerAddedTopping(order_id=new_order.id, topping_type=ToppingType.CHICKEN,
                                     parent_id=customer_started_order.id
                                     ))

        retreived_customer_event = self.customer_event_store.retrieve(customer_added_topping.id)
        assert_that(retreived_customer_event, is_(equal_to(customer_added_topping)))

    def test_delete_order(self):
        new_order = Order().create()
        customer_started_order = self.customer_event_store.create(CustomerStartedOrder(order_id=new_order.id))
        retreived_event = self.customer_event_store.retrieve(customer_started_order.id)
        assert_that(retreived_event, is_(equal_to(customer_started_order)))

        customer_started_order.delete()
        assert_that(
            calling(self.customer_event_store.retrieve).with_args(identifier=customer_started_order.id),
            raises(ModelNotFoundError),
        )
