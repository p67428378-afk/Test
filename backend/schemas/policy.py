
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
import uuid

class PremiumCalculationRequest(BaseModel):
    baseRate: float = Field(..., gt=0)
    ncbTier: str
    vehicleMultiplier: float = Field(..., ge=0.8, le=1.6)

class PremiumCalculationResponse(BaseModel):
    premium: float

class PolicyBase(BaseModel):
    baseRate: float
    ncbTier: str
    ncbDiscount: float
    vehicleMultiplier: float
    finalPremium: float
    vehicleDetails: Dict[str, Any]
    customerDetails: Dict[str, Any]

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    policyId: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

