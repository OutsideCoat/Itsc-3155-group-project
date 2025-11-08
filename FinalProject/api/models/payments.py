from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    cardholder_name = Column(String(120))
    card_last4 = Column(String(4), nullable=False)
    card_brand = Column(String(30))
    payment_type = Column(String(30), nullable=False)
    transaction_status = Column(String(40), nullable=False)
    transaction_reference = Column(String(120))
    paid_at = Column(DateTime, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment")
