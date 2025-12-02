from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import orders as model

def get_daily_revenue(db: Session, target_date: date):
    try:
        start_dt = datetime.combine(target_date, datetime.min.time())
        end_dt = datetime.combine(target_date, datetime.max.time())

        total_revenue = (
            db.query(func.sum(model.Order.total_price))
            .filter(model.Order.order_date >= start_dt, model.Order.order_date <= end_dt)
            .filter((model.Order.status == "Delivered") | (model.Order.status == "Cancelled"))
            .scalar()
        )

        total_revenue = float(total_revenue) if total_revenue is not None else 0.0

        count = (
            db.query(func.count(model.Order.id))
            .filter(model.Order.order_date >= start_dt, model.Order.order_date <= end_dt)
            .filter((model.Order.status == "Delivered") | (model.Order.status == "Cancelled"))
            .scalar()
        )

        return {
            "date": target_date.isoformat(),
            "total_revenue": total_revenue,
            "order_count": int(count or 0)
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)