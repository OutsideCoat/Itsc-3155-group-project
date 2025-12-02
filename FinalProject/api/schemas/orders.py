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
    order_type: Optional[str] = "takeout"


class OrderCreate(BaseModel):
    customer_name: str
    description: str | None  = None
    promo_code: str | None = None


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    total_price: Optional[Decimal] = None
    promo_code: Optional[str] = None
    order_type: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None

    status: str
    tracking_number: Optional[str] = None

    customer: Optional[Customer] = None
    promotion: Optional[Promotion] = None
    payment: Optional[Payment] = None
    order_details: list[OrderDetail] = None
    order_type: str
    

    class ConfigDict:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str
