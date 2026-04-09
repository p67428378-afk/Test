
import pytest
from backend.services.premium_calculator_service import calculate_premium

class MockPremiumCalculationRequest:
    def __init__(self, baseRate, ncbTier, vehicleMultiplier):
        self.baseRate = baseRate
        self.ncbTier = ncbTier
        self.vehicleMultiplier = vehicleMultiplier

def test_calculate_premium_with_base_rate_and_ncb():
    # Test with Tier 1 NCB (20% discount)
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=1.0)
    assert calculate_premium(request) == 400.0

    # Test with Tier 5 NCB (50% discount)
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 5", vehicleMultiplier=1.0)
    assert calculate_premium(request) == 250.0

    # Test with 0% NCB
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 0", vehicleMultiplier=1.0)
    assert calculate_premium(request) == 500.0

    # Test with an invalid NCB tier, should default to 0% discount
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Invalid Tier", vehicleMultiplier=1.0)
    assert calculate_premium(request) == 500.0

    # Test with NCB tier greater than max, should cap at 50%
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 6", vehicleMultiplier=1.0)
    assert calculate_premium(request) == 500.0

def test_apply_vehicle_multipliers():
    # Test with a multiplier of 0.8x
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=0.8)
    assert calculate_premium(request) == 320.0

    # Test with a multiplier of 1.6x
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=1.6)
    assert calculate_premium(request) == 640.0

def test_vehicle_multiplier_edge_cases():
    # Test with a multiplier less than 0.8x, should default to 0.8x
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=0.7)
    assert calculate_premium(request) == 320.0

    # Test with a multiplier greater than 1.6x, should default to 1.6x
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=1.7)
    assert calculate_premium(request) == 640.0

def test_combined_ncb_and_multiplier():
    # Test with Tier 1 NCB and 1.2x multiplier
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 1", vehicleMultiplier=1.2)
    assert calculate_premium(request) == 480.0

    # Test with Tier 5 NCB and 1.5x multiplier
    request = MockPremiumCalculationRequest(baseRate=500, ncbTier="Tier 5", vehicleMultiplier=1.5)
    assert calculate_premium(request) == 375.0
