from sqlalchemy import Boolean, Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(String(255))
    category = Column(String(80))
    #calories = Column(Integer)
    price = Column(DECIMAL(10, 2), nullable=False, server_default='0.0')

    is_vegetarian = Column(Boolean, nullable=False, server_default='0')
    is_gluten_free = Column(Boolean, nullable=False, server_default='0')
    is_vegan = Column(Boolean, nullable=False, server_default='0')
    is_available = Column(Boolean, nullable=False, server_default='1')
    


    # recipes = relationship("Recipe", back_populates="menu_item")
    # order_details = relationship("OrderDetail", back_populates="menu_item")
    # reviews = relationship("Review", back_populates="menu_item")
