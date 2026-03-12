from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)

    bookings = relationship("Booking", back_populates="user")

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    description = Column(String, nullable=True)

    room_types = relationship("RoomType", back_populates="hotel")

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    name = Column(String, index=True) # e.g., "Standard King", "Deluxe Queen"
    description = Column(String, nullable=True)
    max_occupancy = Column(Integer)
    base_price = Column(Float)
    features = Column(String, nullable=True) # Comma-separated features, e.g., "Free Wi-Fi, Mini-bar"

    hotel = relationship("Hotel", back_populates="room_types")
    rooms = relationship("Room", back_populates="room_type")
    inventory = relationship("RoomTypeInventory", back_populates="room_type")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"))
    room_number = Column(String, unique=True, index=True) # e.g., "101", "203A"

    room_type = relationship("RoomType", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    total_price = Column(Float)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    num_guests = Column(Integer)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    amount = Column(Float)
    payment_method = Column(String) # e.g., "Credit Card", "PayPal"
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String, nullable=True)

    booking = relationship("Booking", back_populates="payment")

class RoomTypeInventory(Base):
    __tablename__ = "room_type_inventory"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"))
    date = Column(Date, index=True)
    available_rooms = Column(Integer)
    price_modifier = Column(Float, default=1.0) # e.g., 1.2 for 20% price increase

    room_type = relationship("RoomType", back_populates="inventory")
