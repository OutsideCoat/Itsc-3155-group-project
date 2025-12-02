from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import promotions as promo_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
import uuid
from ..schemas import orders as order_schema

# Keep statuses consistent with schema/model (lower-case)
ALLOWED_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled", "preparing"}


def create(db: Session, request):
    promo_id = None

    if getattr(request, "promo_code", None):
        promo = (
            db.query(promo_model.Promotion)
            .filter(promo_model.Promotion.code == request.promo_code)
            .first()
        )
        if promo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion code not found!"
            )
        if promo.expires_at and promo.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Promotion code has expired!"
            )
        promo_id = promo.id
    
    tracking_number = str(uuid.uuid4()).replace("-", "")[:10]
    order_type = getattr(request, "order_type", None) or "takeout"

    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        promotion_id=promo_id,
        status="pending",
        tracking_number=tracking_number,
        order_type=order_type

    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_filtered(
    db: Session,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    try:
        query = db.query(model.Order)

        if status:
            query = query.filter(model.Order.status == status.lower())
        if start_date:
            start_dt = datetime.combine(start_date, datetime.min.time())
            query = query.filter(model.Order.order_date >= start_dt)
        if end_date:
            end_dt = datetime.combine(end_date, datetime.max.time())
            query = query.filter(model.Order.order_date <= end_date)
        return query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_by_tracking_number(db: Session, tracking_number: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = str(update_data["status"]).lower()
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def update_status(db: Session, item_id: int, new_status: str):
    normalized_status = new_status.lower()
    if normalized_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Allowed statuses are: {', '.join(ALLOWED_STATUSES)}"
        )
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"status": normalized_status}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
