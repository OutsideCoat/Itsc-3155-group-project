from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from sqlalchemy.exc import SQLAlchemyError

from ..models import order_details as model
from ..models import recipes as recipe_model
from ..models import resources as resource_model


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
        if resource.amount < needed:
            shortages.append(
                {
                    "resource_id": resource_id.as_integer_ratio,
                    "name": getattr(resource, "name", None),
                    "needed": needed,
                    "available": resource.amount
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
