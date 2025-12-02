from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas import menu_items as schema
from ..controllers import menu_items as controller

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"],
)

@router.get("/browse", response_model=list[schema.MenuItem])
def browse_menu_items(
    search: str | None = None,
    category: str | None = None,
    is_vegetarian: bool | None = None,
    is_vegan: bool | None = None,
    is_gluten_free: bool | None = None,
    sort_by: str | None = None,      
    sort_order: str = "asc",         
    db: Session = Depends(get_db),
):
    return controller.read_filtered(
        db=db,
        search=search,
        category=category,
        is_vegetarian=is_vegetarian,
        is_vegan=is_vegan,
        is_gluten_free=is_gluten_free,
        sort_by=sort_by,
        sort_order=sort_order
    )