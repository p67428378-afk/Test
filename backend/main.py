from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Guest Room Booking API",
    description="API for searching, booking, and managing guest rooms.",
    version="1.0.0",
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Guest Room Booking API"}

# Placeholder for including other routers (e.g., search, booking, payment)
# from .routers import search, booking, payment
# app.include_router(search.router)
# app.include_router(booking.router)
# app.include_router(payment.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
