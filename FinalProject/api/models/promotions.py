from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    discount_percent = Column(DECIMAL(5, 2), nullable=False, server_default='0.0')
    expires_at = Column(DateTime, nullable=False)

    orders = relationship("Order", back_populates="promotion")
