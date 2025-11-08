from sqlalchemy import Column, ForeignKey, Integer, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    amount = Column(DECIMAL(10, 2), index=True, nullable=False, server_default='0.0')

    menu_item = relationship("MenuItem", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")
