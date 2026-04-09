
from backend.schemas.policy import PremiumCalculationRequest

NCB_DISCOUNT_MAP = {
    "Tier 0": 0.0,
    "Tier 1": 0.20,
    "Tier 2": 0.25,
    "Tier 3": 0.35,
    "Tier 4": 0.45,
    "Tier 5": 0.50,
}

MAX_NCB_DISCOUNT = 0.50
MIN_VEHICLE_MULTIPLIER = 0.8
MAX_VEHICLE_MULTIPLIER = 1.6

def calculate_premium(request: PremiumCalculationRequest) -> float:
    ncb_tier = request.ncbTier
    ncb_discount = NCB_DISCOUNT_MAP.get(ncb_tier, 0.0)

    if ncb_discount > MAX_NCB_DISCOUNT:
        ncb_discount = MAX_NCB_DISCOUNT

    premium_after_ncb = request.baseRate * (1 - ncb_discount)

    vehicle_multiplier = request.vehicleMultiplier
    if vehicle_multiplier < MIN_VEHICLE_MULTIPLIER:
        vehicle_multiplier = MIN_VEHICLE_MULTIPLIER
    elif vehicle_multiplier > MAX_VEHICLE_MULTIPLIER:
        vehicle_multiplier = MAX_VEHICLE_MULTIPLIER

    final_premium = premium_after_ncb * vehicle_multiplier

    return round(final_premium, 2)
