from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import menu_items as model


def create(db: Session, request):
    # Prevent duplicate names
    existing = db.query(model.MenuItem).filter(model.MenuItem.name == request.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Menu item with that name already exists.",
        )
    new_item = model.MenuItem(
        name=request.name,
        description=request.description,
        category=request.category,
        price=request.price,
        is_vegetarian=request.is_vegetarian,
        is_vegan=request.is_vegan,
        is_gluten_free=request.is_gluten_free,
        is_available=request.is_available,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found.")

        update_data = request.dict(exclude_unset=True)

        # If changing the name, ensure uniqueness
        new_name = update_data.get("name")
        if new_name and new_name != current.name:
            exists = db.query(model.MenuItem).filter(model.MenuItem.name == new_name).first()
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item with that name already exists.",
                )

        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )


def delete(db: Session, item_id: int):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found.")
        db.delete(item)
        db.commit()
        return {"message": "Menu item deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )


def read_filtered(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    is_vegetarian: bool | None = None,
    is_vegan: bool | None = None,
    is_gluten_free: bool | None = None,
    sort_by: str | None = None,      
    sort_order: str = "asc",         
):
    try:
        query = db.query(model.MenuItem).filter(model.MenuItem.is_available == True)

        if search:
            like = f"%{search}%"
            query = query.filter(model.MenuItem.name.ilike(like))

        if category:
            query = query.filter(model.MenuItem.category == category)

        if is_vegetarian is not None:
            query = query.filter(model.MenuItem.is_vegetarian == is_vegetarian)

        if is_vegan is not None:
            query = query.filter(model.MenuItem.is_vegan == is_vegan)

        if is_gluten_free is not None:
            query = query.filter(model.MenuItem.is_gluten_free == is_gluten_free)

        
        if sort_by == "name":
            sort_column = model.MenuItem.name
        elif sort_by == "price":
            sort_column = model.MenuItem.price
        else:
            sort_column = None

        if sort_column is not None:
            if sort_order == "desc":
                sort_column = sort_column.desc()
            query = query.order_by(sort_column)

        return query.all()

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
