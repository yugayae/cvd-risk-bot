
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
import json

MODEL_PATH = "model/improved_catboost.cbm"

def create_base_patient():
    """Returns a 'healthy' baseline patient: 45 years male, non-smoker, active, normal BP/gluc/chol."""
    return {
        "age": 45 * 365,
        "gender": 2,
        "height": 175,
        "weight": 70,
        "ap_hi": 120,
        "ap_lo": 80,
        "cholesterol": 1,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1,
        "bmi": 70 / (1.75**2)
    }

def get_prediction(model, p_dict):
    features = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    X = pd.DataFrame([p_dict])[features]
    return float(model.predict_proba(X)[0, 1])

def run_tests():
    model = CatBoostClassifier()
    model.load_model("c:/HomeWork/Medical/CVD_risk_Cat_Boost/cvd-risk-api/" + MODEL_PATH)
    
    base = create_base_patient()
    base_risk = get_prediction(model, base)
    
    results = []
    
    # 1. Smoking
    p_smoke = base.copy()
    p_smoke['smoke'] = 1
    smoke_risk = get_prediction(model, p_smoke)
    results.append({
        "factor": "Smoking",
        "base_val": 0,
        "test_val": 1,
        "base_risk": base_risk,
        "test_risk": smoke_risk,
        "delta": smoke_risk - base_risk,
        "is_paradox": (smoke_risk < base_risk)
    })
    
    # 2. Glucose
    p_gluc = base.copy()
    p_gluc['gluc'] = 3 # Well above normal
    gluc_risk = get_prediction(model, p_gluc)
    results.append({
        "factor": "Glucose (High)",
        "base_val": 1,
        "test_val": 3,
        "base_risk": base_risk,
        "test_risk": gluc_risk,
        "delta": gluc_risk - base_risk,
        "is_paradox": (gluc_risk < base_risk)
    })
    
    # 3. Cholesterol
    p_chol = base.copy()
    p_chol['cholesterol'] = 3 # High
    chol_risk = get_prediction(model, p_chol)
    results.append({
        "factor": "Cholesterol (High)",
        "base_val": 1,
        "test_val": 3,
        "base_risk": base_risk,
        "test_risk": chol_risk,
        "delta": chol_risk - base_risk,
        "is_paradox": (chol_risk < base_risk)
    })
    
    # 4. Activity
    p_lazy = base.copy()
    p_lazy['active'] = 0 # Inactive
    lazy_risk = get_prediction(model, p_lazy)
    # Medical logic: Inactive should have higher risk than Active
    results.append({
        "factor": "Physical Activity (Inactive)",
        "base_val": 1,
        "test_val": 0,
        "base_risk": base_risk,
        "test_risk": lazy_risk,
        "delta": lazy_risk - base_risk,
        "is_paradox": (lazy_risk < base_risk)
    })

    # 5. Alcohol (often paradoxal in some datasets due to light-moderate drinkers having better health than abstainers)
    p_alco = base.copy()
    p_alco['alco'] = 1
    alco_risk = get_prediction(model, p_alco)
    results.append({
        "factor": "Alcohol",
        "base_val": 0,
        "test_val": 1,
        "base_risk": base_risk,
        "test_risk": alco_risk,
        "delta": alco_risk - base_risk,
        "is_paradox": (alco_risk < base_risk)
    })
    
    # 6. Systolic BP
    p_bp = base.copy()
    p_bp['ap_hi'] = 150
    bp_risk = get_prediction(model, p_bp)
    results.append({
        "factor": "Systolic BP (150)",
        "base_val": 120,
        "test_val": 150,
        "base_risk": base_risk,
        "test_risk": bp_risk,
        "delta": bp_risk - base_risk,
        "is_paradox": (bp_risk < base_risk)
    })

    # Saving results
    with open("c:/HomeWork/Medical/CVD_risk_Cat_Boost/cvd-risk-api/model/clinical_paradoxes.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("Clinical paradox stress test completed.")

if __name__ == "__main__":
    run_tests()
