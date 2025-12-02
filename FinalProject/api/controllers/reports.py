from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import orders as model
from ..models import order_details as order_detail_model
from ..models import sandwiches as sandwich_model
from ..models import menu_items as menu_model
from ..models import reviews as review_model
from ..schemas import reports as report_model  


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
    
def get_dish_popularity(db: Session, start_date: date, end_date: date, limit: int = 5):
    try:
        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())
        
        base_query = (
            db.query(
                sandwich_model.Sandwich.id.label("sandwich_id"),
                sandwich_model.Sandwich.sandwich_name.label("sandwich_name"),
                func.sum(order_detail_model.OrderDetail.amount).label("total_ordered")
            )
            .join(
                order_detail_model.OrderDetail,
                order_detail_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id
            )
            .group_by(
                sandwich_model.Sandwich.id,
                sandwich_model.Sandwich.sandwich_name
            )
            
        )

        most_ordered_query = (
            base_query.order_by(func.sum(order_detail_model.OrderDetail.amount).desc())
            .limit(limit)
            .all()
        )

        least_ordered_query = (
            base_query.order_by(func.sum(order_detail_model.OrderDetail.amount).asc())
            .limit(limit)
            .all()
        )

        def row_to_dict(row):
            return {
                "sandwich_id": row.sandwich_id,
                "sandwich_name": row.sandwich_name,
                "total_ordered": int(row.total_ordered)
            }
        
        return {
            "most_ordered": [row_to_dict(row) for row in most_ordered_query],
            "least_ordered": [row_to_dict(row) for row in least_ordered_query]
        }
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
def get_review_trends(db: Session, min_reviews: int = 1, limit: int = 10) -> list[report_model.ReviewTrend]:
    try:
        query = (
            db.query(
                menu_model.MenuItem.id.label("menu_item_id"),
                menu_model.MenuItem.name.label("menu_item_name"),
                func.avg(review_model.Review.rating).label("average_rating"),
                func.count(review_model.Review.id).label("review_count"),
                func.max(review_model.Review.created_at).label("last_review_date")
            )
            .join(
                review_model.Review, 
                review_model.Review.menu_item_id == menu_model.MenuItem.id
            )
            .group_by(
                menu_model.MenuItem.id,
                menu_model.MenuItem.name
            )
            .having(func.count(review_model.Review.id) >= min_reviews)
            .order_by(func.avg(review_model.Review.rating).desc())
            .limit(limit)
        )

        rows = query.all()

        return [
            report_model.ReviewTrend(
                menu_item_id=row.menu_item_id,
                menu_item_name=row.menu_item_name,
                average_rating=float(row.average_rating),
                review_count=row.review_count,
                last_review_date=row.last_review_date
            )
            for row in rows
        ]
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    