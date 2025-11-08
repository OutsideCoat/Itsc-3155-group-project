from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    order_id: int
    cardholder_name: Optional[str] = None
    card_last4: str
    card_brand: Optional[str] = None
    payment_type: str
    transaction_status: str
    transaction_reference: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    cardholder_name: Optional[str] = None
    card_last4: Optional[str] = None
    card_brand: Optional[str] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    transaction_reference: Optional[str] = None


class Payment(PaymentBase):
    id: int
    paid_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
