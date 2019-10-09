from collections import namedtuple
from enum import Enum, unique

from microcosm_postgres.models import EntityMixin, Model
from microcosm_postgres.types import EnumType
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy_utils import UUIDType


@unique
class ToppingType(Enum):
    HAM = "Ham"
    CHICKEN = "Chicken"
    PINEAPPLE = "Pineapple"
    BLACK_OLIVES = "Black Olives"
    ONIONS = "Onions"

    def __str__(self):
        return self.name


class Topping(EntityMixin, Model):
    __tablename__ = "topping"

    pizza_id = Column(UUIDType(), ForeignKey("pizza.id"), nullable=False)
    topping_type = Column(EnumType(ToppingType), nullable=False)

    __table_args__ = (
        Index(
            "constraint_pizza_id_idx",
            pizza_id,
        ),
        Index(
            "unique_topping",
            pizza_id,
            topping_type,
            unique=True,
        ),
    )
