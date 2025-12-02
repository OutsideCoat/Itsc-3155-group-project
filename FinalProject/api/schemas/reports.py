from typing import Optional, List
from pydantic import BaseModel

class DishStatistics(BaseModel):
    sandwich_id: int
    sandwich_name: str
    total_ordered: int

class DishPopularityResponse(BaseModel):
    most_ordered: List[DishStatistics]
    least_ordered: List[DishStatistics]



