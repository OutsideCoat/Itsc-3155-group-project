from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_percent: Decimal = Decimal("0.0")
    expires_at: datetime


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    discount_percent: Optional[Decimal] = None
    expires_at: Optional[datetime] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
