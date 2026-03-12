from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional
from .models import BookingStatus, PaymentStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

# Hotel Schemas
class HotelBase(BaseModel):
    name: str
    address: str
    city: str
    country: str
    description: Optional[str] = None

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int
    room_types: List['RoomTypeResponse'] = []

    class Config:
        from_attributes = True

# RoomType Schemas
class RoomTypeBase(BaseModel):
    name: str
    max_occupancy: int
    base_price: float
    description: Optional[str] = None
    features: Optional[str] = None

class RoomTypeCreate(RoomTypeBase):
    hotel_id: int

class RoomTypeResponse(RoomTypeBase):
    id: int
    hotel_id: int

    class Config:
        from_attributes = True

# Room Schemas
class RoomBase(BaseModel):
    room_number: str

class RoomCreate(RoomBase):
    room_type_id: int

class RoomResponse(RoomBase):
    id: int
    room_type_id: int

    class Config:
        from_attributes = True

# Booking Schemas
class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    num_guests: int

class BookingCreate(BookingBase):
    room_id: int
    user_id: int
    total_price: float

class BookingResponse(BookingBase):
    id: int
    user_id: int
    room_id: int
    total_price: float
    status: BookingStatus

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentBase(BaseModel):
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    booking_id: int

class PaymentResponse(PaymentBase):
    id: int
    booking_id: int
    status: PaymentStatus
    transaction_id: Optional[str] = None

    class Config:
        from_attributes = True

# Room Search Schema
class RoomSearch(BaseModel):
    check_in_date: date
    check_out_date: date
    num_guests: int
    city: Optional[str] = None
    country: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

# Update forward refs for HotelResponse
HotelResponse.model_rebuild()
