from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas import menu_items as schema
from ..controllers import menu_items as controller

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"],
)

@router.post("/", response_model=schema.MenuItem)
def create_menu_item(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update_menu_item(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


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
