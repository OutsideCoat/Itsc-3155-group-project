from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import promotions as controller
from ..schemas import promotions as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)

@router.post("/", response_model=schema.Promotion)
def create_promotion(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Promotion])
def get_all_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Promotion)
def get_promotion(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.Promotion)
def update_promotion(item_id: int, request: schema.PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)

