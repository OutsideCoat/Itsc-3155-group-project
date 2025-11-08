from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    calories: Optional[int] = None
    price: Decimal = Decimal("0.0")


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    calories: Optional[int] = None
    price: Optional[Decimal] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
