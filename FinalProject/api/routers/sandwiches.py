from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/sandwiches",
    tags=["Sandwiches"]
)

@router.post("/", response_model=schema.Sandwich)
def create_sandwich(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)
        

@router.get("/", response_model=list[schema.Sandwich])
def get_all_sandwiches(db: Session = Depends(get_db)):
    return controller.read_all(db)  

@router.get("/{item_id}", response_model=schema.Sandwich)
def get_sandwich(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.Sandwich)
def update_sandwich(item_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)

@router.delete("/{item_id}", status_code=204)
def delete_sandwich(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)

