from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    #calories: Optional[int] = None
    price: Decimal = Decimal("0.0")
    is_vegetarian: bool = False
    is_gluten_free: bool = False
    is_vegan: bool = False
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    #calories: Optional[int] = None
    price: Optional[Decimal] = None
    is_vegetarian: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
