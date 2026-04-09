
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app import app
from backend.core.database import Base, get_db
from unittest.mock import patch

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_calculate_premium_endpoint():
    response = client.post(
        "/api/v1/insurance/premium/calculate",
        json={"baseRate": 500, "ncbTier": "Tier 1", "vehicleMultiplier": 1.2},
    )
    assert response.status_code == 200
    assert response.json() == {"premium": 480.0}

def test_calculate_premium_endpoint_invalid_input():
    response = client.post(
        "/api/v1/insurance/premium/calculate",
        json={"baseRate": -500, "ncbTier": "Tier 1", "vehicleMultiplier": 1.2},
    )
    assert response.status_code == 422  # pydantic validation error

    response = client.post(
        "/api/v1/insurance/premium/calculate",
        json={"baseRate": 500, "ncbTier": "Tier 1", "vehicleMultiplier": 0.7},
    )
    assert response.status_code == 422  # pydantic validation error

    response = client.post(
        "/api/v1/insurance/premium/calculate",
        json={"baseRate": 500, "ncbTier": "Tier 1", "vehicleMultiplier": 1.7},
    )
    assert response.status_code == 422  # pydantic validation error

@patch('backend.routers.insurance.calculate_premium')
def test_calculate_premium_endpoint_exception(mock_calculate_premium):
    mock_calculate_premium.side_effect = Exception("Test Exception")
    response = client.post(
        "/api/v1/insurance/premium/calculate",
        json={"baseRate": 500, "ncbTier": "Tier 1", "vehicleMultiplier": 1.2},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Test Exception"}
