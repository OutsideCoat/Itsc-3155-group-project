from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from sqlalchemy.exc import SQLAlchemyError

from ..models import order_details as model
from ..models import recipes as recipe_model
from ..models import resources as resource_model
from ..models import menu_items as menu_model
from ..models import orders as order_model
from ..models import promotions as promo_model


def create(db: Session, request):
    required_by_resource: dict[int, int] = {}
    recipes = (
        db.query(recipe_model.Recipe)
        .filter(recipe_model.Recipe.menu_item_id == request.menu_item_id)
        .all()
    )
    for recipe in recipes:
        needed = recipe.amount * request.amount
        required_by_resource[recipe.resource_id] = (
            required_by_resource.get(recipe.resource_id, 0) + needed
        )
    shortages = []
    for resource_id, required_amount in required_by_resource.items():
        resource = (
            db.query(resource_model.Resource)
            .filter(resource_model.Resource.id == resource_id)
            .first()
        )
        if resource is None:
            shortages.append({"resource_id": resource_id, "message": "Resource not found"})
            continue
        if resource.amount < required_amount:
            shortages.append(
                {
                    "resource_id": resource_id,
                    "item": getattr(resource, "item", None),
                    "needed": float(required_amount),
                    "available": float(resource.amount)
                }
            )
    if shortages:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Insufficient resources", "shortages": shortages}
        )
    for resource_id, needed in required_by_resource.items():
        resource = (
            db.query(resource_model.Resource).filter(resource_model.Resource.id == resource_id).with_for_update().first()

        )
        resource.amount -= needed

    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        amount=request.amount
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    try:
        order = (
            db.query(order_model.Order)
            .filter(order_model.Order.id == request.order_id)
            .first()
        )
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Id not found!")
        
        details = (
            db.query(model.OrderDetail)
            .filter(model.OrderDetail.order_id == request.order_id)
            .all()
        )
        subtotal = 0
        for detail in details:
            menu_item = (
                db.query(menu_model.MenuItem)
                .filter(menu_model.MenuItem.id == detail.menu_item_id)
                .first()
            )
            if menu_item:
                subtotal += float(menu_item.price * detail.amount)
        discount_percent = 0.0

        if getattr(order, "promotion_id", None):
            promotion = (
                db.query(promo_model.Promotion)
                .filter(promo_model.Promotion.id == order.promotion_id)
                .first()
            )
            if promotion:
                discount_percent = float(promotion.discount_percent)

        final_total = subtotal * (1 - discount_percent / 100)
        order.total_price = final_total
        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)



    return new_item
        

def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
