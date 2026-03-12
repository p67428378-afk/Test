from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing import List, Optional

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # In a real application, you would hash the password here
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Hotel CRUD
def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).offset(skip).limit(limit).all()

def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(**hotel.model_dump())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

# RoomType CRUD
def get_room_type(db: Session, room_type_id: int):
    return db.query(models.RoomType).filter(models.RoomType.id == room_type_id).first()

def get_room_types(db: Session, hotel_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.RoomType)
    if hotel_id:
        query = query.filter(models.RoomType.hotel_id == hotel_id)
    return query.offset(skip).limit(limit).all()

def create_room_type(db: Session, room_type: schemas.RoomTypeCreate):
    db_room_type = models.RoomType(**room_type.model_dump())
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type

# Room CRUD
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session, room_type_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Room)
    if room_type_id:
        query = query.filter(models.Room.room_type_id == room_type_id)
    return query.offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# Booking CRUD
def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Booking)
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def update_booking_status(db: Session, booking_id: int, new_status: models.BookingStatus):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking:
        db_booking.status = new_status
        db.commit()
        db.refresh(db_booking)
    return db_booking

# Payment CRUD
def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_payments_for_booking(db: Session, booking_id: int):
    return db.query(models.Payment).filter(models.Payment.booking_id == booking_id).first()

def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment_status(db: Session, payment_id: int, new_status: models.PaymentStatus, transaction_id: Optional[str] = None):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment:
        db_payment.status = new_status
        if transaction_id:
            db_payment.transaction_id = transaction_id
        db.commit()
        db.refresh(db_payment)
    return db_payment

# Room Search Logic
def search_available_rooms(
    db: Session,
    search_params: schemas.RoomSearch
) -> List[models.RoomType]:
    # This is a simplified search logic. A real implementation would be more complex
    # and involve checking room_type_inventory for actual availability.
    # For now, it filters room types based on occupancy and optionally location/price.

    query = db.query(models.RoomType).join(models.Hotel)

    if search_params.city:
        query = query.filter(models.Hotel.city == search_params.city)
    if search_params.country:
        query = query.filter(models.Hotel.country == search_params.country)
    if search_params.min_price:
        query = query.filter(models.RoomType.base_price >= search_params.min_price)
    if search_params.max_price:
        query = query.filter(models.RoomType.base_price <= search_params.max_price)

    # Filter by max_occupancy
    query = query.filter(models.RoomType.max_occupancy >= search_params.num_guests)

    # This part needs significant enhancement for actual date-based availability checking
    # For now, it just returns room types that match the basic criteria.
    # A proper implementation would involve querying RoomTypeInventory for the given date range.

    return query.all()
