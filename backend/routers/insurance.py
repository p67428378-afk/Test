
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.policy import PremiumCalculationRequest, PremiumCalculationResponse
from backend.services.premium_calculator_service import calculate_premium
from backend.core.database import get_db
from backend.models.policy import Policy

router = APIRouter()

@router.post("/premium/calculate", response_model=PremiumCalculationResponse)
def calculate_premium_endpoint(request: PremiumCalculationRequest, db: Session = Depends(get_db)):
    try:
        premium = calculate_premium(request)
        # Optionally, you can save the calculation to the database
        # policy = Policy(
        #     baseRate=request.baseRate,
        #     ncbTier=request.ncbTier,
        #     ncbDiscount=NCB_DISCOUNT_MAP.get(request.ncbTier, 0.0),
        #     vehicleMultiplier=request.vehicleMultiplier,
        #     finalPremium=premium,
        #     vehicleDetails={},
        #     customerDetails={}
        # )
        # db.add(policy)
        # db.commit()
        # db.refresh(policy)
        return PremiumCalculationResponse(premium=premium)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
