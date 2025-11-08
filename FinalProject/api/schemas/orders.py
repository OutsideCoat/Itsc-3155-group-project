from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .order_details import OrderDetail
from .customers import Customer
from .payments import Payment
from .promotions import Promotion


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[OrderStatus] = OrderStatus.pending
    total_price: Decimal = Decimal("0.0")


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    total_price: Optional[Decimal] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    customer: Optional[Customer] = None
    promotion: Optional[Promotion] = None
    payment: Optional[Payment] = None
    order_details: list[OrderDetail] = Field(default_factory=list)

    class ConfigDict:
        from_attributes = True
