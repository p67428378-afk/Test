from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # In a real scenario, you'd perform availability checks here before creating a booking
    return crud.create_booking(db=db, booking=booking)

@router.get("/", response_model=List[schemas.BookingResponse])
def read_bookings(user_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, user_id=user_id, skip=skip, limit=limit)
    return bookings

@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(
    booking_id: int,
    new_status: models.BookingStatus,
    db: Session = Depends(get_db)
):
    db_booking = crud.update_booking_status(db, booking_id, new_status)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking
