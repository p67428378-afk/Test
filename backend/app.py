
from fastapi import FastAPI
from backend.routers import insurance
from backend.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(insurance.router, prefix="/api/v1/insurance", tags=["insurance"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

