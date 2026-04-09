
import uuid
from sqlalchemy import Column, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from backend.core.database import Base

class Policy(Base):
    __tablename__ = "policies"

    policyId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    baseRate = Column(Float)
    ncbTier = Column(String)
    ncbDiscount = Column(Float)
    vehicleMultiplier = Column(Float)
    finalPremium = Column(Float)
    vehicleDetails = Column(JSON)
    customerDetails = Column(JSON)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
