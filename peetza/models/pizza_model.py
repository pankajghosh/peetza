"""
An example model.

"""
from collections import namedtuple
from enum import unique, Enum

from microcosm_postgres.models import EntityMixin, Model
from microcosm_postgres.types import EnumType
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

PizzaTypeInfo = namedtuple(
    "PizzaTypeInfo",
    [
        "value",
        "description",
    ],
)

@unique
class PizzaType(Enum):
    def __str__(self):
        return self.name

    HANDTOSSED = PizzaTypeInfo(
        "HandTossed",
        "Garlic-seasoned crust with a rich, buttery taste.",
    )
    BROOKLYNSTYLE = PizzaTypeInfo(
        "Brooklyn Style",
        "Hand stretched to be big, thin and perfectly foldable.",
    )
    GLUTENFREECRUST = PizzaTypeInfo(
        "Gluten Free Crust",
        "pizza made with a Gluten Free Crust."
    )


@unique
class PizzaSize(Enum):
    SMALL = "Small - 10 in"
    MEDIUM = "Medium - 12 in"
    LARGE = "Large - 14 in"
    X_LARGE = "X-Large - 16 in"

    def __str__(self):
        return self.name


class Pizza(EntityMixin, Model):
    """
    An example has a unique name.

    """
    __tablename__ = "pizza"

    pizza_size = Column(EnumType(PizzaSize), nullable=False)
    pizza_type = Column(EnumType(PizzaType), nullable=False)