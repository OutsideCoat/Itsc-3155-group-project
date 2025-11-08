from . import (
    orders,
    order_details,
    recipes,
    menu_items,
    resources,
    customers,
    payments,
    promotions,
    reviews,
)

from ..dependencies.database import Base, engine


def index():
    Base.metadata.create_all(engine)
