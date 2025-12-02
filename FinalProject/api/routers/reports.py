from datetime import date, datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import reports as controller

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/daily-revenue/", response_model=dict)
def get_daily_revenue(target_date: date, db: Session = Depends(get_db)):
    return controller.get_daily_revenue(db, target_date)