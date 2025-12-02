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


#def index():
    #Base.metadata.create_all(engine)

def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
