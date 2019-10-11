from microcosm_eventsource.models import EventMeta
from microcosm_postgres.models import UnixTimestampEntityMixin
from microcosm_postgres.types import EnumType
from sqlalchemy import Column
from sqlalchemy_utils import UUIDType

from peetza.models.customer_event_type import CustomerEventType
from peetza.models.order_model import Order
from peetza.models.pizza_model import PizzaSize, PizzaType
from peetza.models.topping_model import ToppingType


class CustomerEvent(UnixTimestampEntityMixin, metaclass=EventMeta):
    __tablename__ = "customer_event"
    __eventtype__ = CustomerEventType
    __container__ = Order

    order_id = Column(UUIDType, nullable=True)
    pizza_id = Column(UUIDType, nullable=True)
    pizza_type = Column(EnumType(PizzaType), nullable=True)
    pizza_size = Column(EnumType(PizzaSize), nullable=True)
    topping_type = Column(EnumType(ToppingType), nullable=True)

    __mapper_args__ = dict(
        polymorphic_on="event_type",
    )


class CustomerStartedOrder(CustomerEvent):
    __mapper_args__ = {
        "polymorphic_identity": CustomerEventType.CustomerStartedOrder,
    }


class CustomerStartedPizza(CustomerEvent):
    __mapper_args__ = {
        "polymorphic_identity": CustomerEventType.CustomerStartedPizza,
    }


class CustomerChosePizzaType(CustomerEvent):
    __mapper_args__ = {
        "polymorphic_identity": CustomerEventType.CustomerChosePizzaType,
    }


class CustomerAddedTopping(CustomerEvent):
    __mapper_args__ = {
        "polymorphic_identity": CustomerEventType.CustomerAddedTopping,
    }


class CustomerFinalizedPizza(CustomerEvent):
    __mapper_args__ = {
        "polymorphic_identity": CustomerEventType.CustomerFinalizedPizza,
    }
