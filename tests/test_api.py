from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Verify that the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_endpoint_valid_case():
    """Verify prediction with valid inputs."""
    payload = {
        "age_years": 50,
        "height": 175,
        "weight": 80,
        "ap_hi": 120,
        "ap_lo": 80,
        "cholesterol": 1,
        "active": 1,
        "smoke": 0,
        "alco": 0,
        "gluc": 1,
        "gender": 2,
        "ui_language": "en"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_probability" in data
    assert "risk_category" in data
    # Check that new validation logic (BMI calc) works
    assert data["patient_bmi"] == round(80 / (1.75 ** 2), 1)

def test_predict_endpoint_invalid_input():
    """Verify that invalid inputs (e.g., too young) raise 422 validation errors."""
    payload = {
        "age_years": 10,  # Invalid: < 18
        "height": 175,
        "weight": 80,
        "ap_hi": 120,
        "ap_lo": 80,
        "cholesterol": 1,
        "active": 1,
        "smoke": 0,
        "alco": 0,
        "gluc": 1,
        "gender": 2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
