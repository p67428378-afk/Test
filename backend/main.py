from fastapi import FastAPI
from dotenv import load_dotenv
import os

from . import models
from .database import engine

# Load environment variables from .env file
load_dotenv()

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Guest Room Booking API",
    description="API for searching, booking, and managing guest rooms.",
    version="1.0.0",
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Guest Room Booking API"}

# Including other routers
from .routers import users, hotels, room_types, rooms, bookings, payments, search

app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(room_types.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(search.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
