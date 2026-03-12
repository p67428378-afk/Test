from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.PaymentResponse)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # In a real scenario, this would integrate with a payment gateway
    return crud.create_payment(db=db, payment=payment)

@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}/status", response_model=schemas.PaymentResponse)
def update_payment_status(
    payment_id: int,
    new_status: models.PaymentStatus,
    transaction_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    db_payment = crud.update_payment_status(db, payment_id, new_status, transaction_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment
