from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.HotelResponse)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    return crud.create_hotel(db=db, hotel=hotel)

@router.get("/", response_model=List[schemas.HotelResponse])
def read_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hotels = crud.get_hotels(db, skip=skip, limit=limit)
    return hotels

@router.get("/{hotel_id}", response_model=schemas.HotelResponse)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = crud.get_hotel(db, hotel_id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel
