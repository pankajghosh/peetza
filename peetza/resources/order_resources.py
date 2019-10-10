"""
Example resources.

"""
from marshmallow import Schema, fields
from microcosm_flask.linking import Link, Links
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation

from peetza.models.order_model import Order


class NewOrderSchema(Schema):
    pass


class OrderSchema(NewOrderSchema):
    id = fields.UUID(required=True)

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
        # links["child:pizza"] = Link.for_(
        #     Operation.Retrieve,
        #     Namespace(
        #         subject=Pizza,
        #         version="v1",
        #     ),
        #     pizza_id=obj.pizza_id,
        # )
        return links.to_dict()
