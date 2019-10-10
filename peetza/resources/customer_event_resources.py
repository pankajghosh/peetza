"""
Example resources.

"""
from marshmallow import Schema, fields
from microcosm_eventsource.resources import EventSchema
from microcosm_flask.fields import EnumField
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation

from peetza.models.customer_event_type import CustomerEventType
from peetza.models.order_model import Order
from peetza.models.pizza_model import PizzaSize, PizzaType
from peetza.models.topping_model import ToppingType


class NewCustomerEventSchema(Schema):
    eventType = EnumField(
        CustomerEventType,
        attribute="event_type",
        required=True,
    )
    pizza_id = fields.UUID()
    order_id = fields.UUID()

    pizza_size = EnumField(PizzaSize)
    pizza_type = EnumField(PizzaType)
    topping_type = EnumField(ToppingType)


class CustomerEventSchema(NewCustomerEventSchema, EventSchema):
    id = fields.UUID(required=True)

    createdAt = fields.Float(
        attribute="created_at",
        required=True,
    )

    _links = fields.Method(
        "get_links",
        dump_only=True,
    )

    def get_links(self, obj):
        links = Links()
        links["self"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=Order,
                version="v1",
            ),
            order_id=obj.id,
        )
        return links.to_dict()
