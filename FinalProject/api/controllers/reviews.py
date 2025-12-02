from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, asc

from ..models import reviews as model
from ..models import menu_items as menu_model

def create_review(db: Session, request):
    menu_item = (
        db.query(menu_model.MenuItem)
        .filter(menu_model.MenuItem.id == request.menu_item_id)
        .first()
    )
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {request.menu_item_id} not found.",
        )
    
    new_item = model.Review(
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment,
        customer_name=request.customer_name
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return new_item

def read_reviews_by_menu_item(db: Session, menu_item_id: int):
    try:
        reviews = (
            db.query(model.Review)
            .filter(model.Review.menu_item_id == menu_item_id)
            .order_by(desc(model.Review.created_at))
            .all()
        )
        return reviews
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
        
    