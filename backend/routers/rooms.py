from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)

@router.get("/", response_model=List[schemas.RoomResponse])
def read_rooms(room_type_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, room_type_id=room_type_id, skip=skip, limit=limit)
    return rooms

@router.get("/{room_id}", response_model=schemas.RoomResponse)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
