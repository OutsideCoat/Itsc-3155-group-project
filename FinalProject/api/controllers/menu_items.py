from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import menu_items as model


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
