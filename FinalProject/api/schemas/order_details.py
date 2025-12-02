from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .menu_items import MenuItem


class OrderDetailBase(BaseModel):
    amount: int
    order_id: int
    sandwich_id: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_item: MenuItem = None

    class ConfigDict:
        from_attributes = True
