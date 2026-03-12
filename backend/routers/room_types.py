from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/room_types",
    tags=["Room Types"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.RoomTypeResponse)
def create_room_type(room_type: schemas.RoomTypeCreate, db: Session = Depends(get_db)):
    return crud.create_room_type(db=db, room_type=room_type)

@router.get("/", response_model=List[schemas.RoomTypeResponse])
def read_room_types(hotel_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    room_types = crud.get_room_types(db, hotel_id=hotel_id, skip=skip, limit=limit)
    return room_types

@router.get("/{room_type_id}", response_model=schemas.RoomTypeResponse)
def read_room_type(room_type_id: int, db: Session = Depends(get_db)):
    db_room_type = crud.get_room_type(db, room_type_id=room_type_id)
    if db_room_type is None:
        raise HTTPException(status_code=404, detail="Room Type not found")
    return db_room_type
