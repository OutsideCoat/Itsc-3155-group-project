from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DateTime, nullable=False, server_default=func.now())
    description = Column(String(300))
    tracking_number = Column(String(64), unique=True, nullable=True)
    status = Column(String(50), nullable=False, server_default="pending")
    total_price = Column(DECIMAL(10, 2), nullable=False, server_default='0.0')
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
    customer = relationship("Customer", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
