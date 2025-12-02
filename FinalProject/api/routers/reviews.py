from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas import reviews as schema
from ..controllers import reviews as controller

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)

@router.post("/", response_model=schema.Review)
def create_review(
    request: schema.ReviewCreate,
    db: Session = Depends(get_db),
):
    return controller.create_review(db=db, request=request)

@router.get("/menu-item/{menu_item_id}", response_model=list[schema.Review])
def get_reviews_by_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    return controller.read_reviews_by_menu_item(db=db, menu_item_id=menu_item_id)

