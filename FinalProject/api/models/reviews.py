from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(120), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    comment = Column(String(1000), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    #customer = relationship("Customer", back_populates="reviews")
    #menu_item = relationship("MenuItem", back_populates="reviews")
