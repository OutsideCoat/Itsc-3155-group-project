from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(30))
    address = Column(String(255))

    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
