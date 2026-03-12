from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)

@router.post("/rooms", response_model=List[schemas.RoomTypeResponse])
def search_rooms(search_params: schemas.RoomSearch, db: Session = Depends(get_db)):
    available_room_types = crud.search_available_rooms(db, search_params)
    if not available_room_types:
        raise HTTPException(status_code=404, detail="No rooms found for the given criteria")
    return available_room_types
