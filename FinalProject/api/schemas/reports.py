import decimal
from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime, date

class DishStatistics(BaseModel):
    menu_item_id: int
    menu_item_name: str
    total_ordered: int

class DishPopularityResponse(BaseModel):
    most_ordered: List[DishStatistics]
    least_ordered: List[DishStatistics]

class ReviewTrend(BaseModel):
    menu_item_id: int
    average_rating: decimal.Decimal
    menu_item_name: Optional[str] = None
    review_count: int
    last_review_date: datetime | None


