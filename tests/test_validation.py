import pytest
from pydantic import ValidationError
from app.schemas import PatientInput

def test_valid_patient_input():
    """Test creating a valid PatientInput object."""
    input_data = PatientInput(
        age_years=45,
        height=170,
        weight=70,
        ap_hi=120,
        ap_lo=80,
        cholesterol=1,
        active=1,
        smoke=0,
        alco=0,
        gluc=1,
        gender=1
    )
    assert input_data.age_years == 45
    # Auto-calculated BMI
    assert input_data.bmi == round(70 / (1.7**2), 2)

def test_invalid_bp_logic():
    """Test that systolic < diastolic raises error."""
    with pytest.raises(ValidationError) as exc:
        PatientInput(
            age_years=45,
            height=170,
            weight=70,
            ap_hi=100,
            ap_lo=120, # Invalid
            cholesterol=1,
            active=1,
            smoke=0,
            alco=0,
            gluc=1,
            gender=1
        )
    assert "Systolic pressure (ap_hi) must be higher than diastolic (ap_lo)" in str(exc.value)

def test_age_restrictions():
    """Test age boundaries."""
    # Too young
    with pytest.raises(ValidationError):
        PatientInput(
            age_years=10, 
            height=170, weight=70, ap_hi=120, ap_lo=80,
            cholesterol=1, active=1, smoke=0, alco=0, gluc=1, gender=1
        )
