from localization import t
from localization import LOCALIZATION
from clinical_mapping import CLINICAL_FEATURE_MAP
import pandas as pd
from localization import t
from shap_explainer import explain_patient
from shap_interpreter import interpret_shap
from safety import collect_safety_warnings
from risk_card import build_risk_card
from audit import build_audit_block
from model_loader import get_model_performance_metrics

CLINICAL_PRIORITY = {
    "high_bp": 1,
    "obesity": 2,
    "cholesterol_high": 3,
    "cholesterol_attention": 4,

    "age_years": 5,
    "bmi": 6,
    "ap_hi": 7,
    "ap_lo": 8,

    "smoke": 9,
    "gluc": 10,
    "alco": 11,
    "active": 12,
}

def categorize_risk(probability: float) -> str:
    if probability < 0.10:
        return "low"
    elif probability < 0.20:
        return "moderate"
    else:
        return "high"

def collect_rule_based_flags(patient):
    flags = []

    if patient.ap_hi >= 140:
        flags.append("high_bp")

    if patient.bmi >= 30:
        flags.append("obesity")

    if patient.cholesterol == 2:
        flags.append("cholesterol_attention")

    if patient.cholesterol == 3:
        flags.append("cholesterol_high")

    return flags


def assess_prediction_confidence(probability: float) -> dict:
    thresholds = [0.10, 0.20]
    distance = min(abs(probability - t) for t in thresholds)

    if distance >= 0.07:
        level = "high"
    elif distance >= 0.03:
        level = "moderate"
    else:
        level = "low"

    return {
        "confidence_level": level
    }

def collect_clinical_risk_factors(patient, lang: str) -> list:
    factors = []

    def add(feature_key):
        loc = LOCALIZATION[lang]["shap_factors"].get(feature_key)
        
        if not loc:
            return

        factors.append({
            "key": feature_key,
            "factor": loc["name"],
            "direction": "increases",
            "clinical_note": loc["note"]
        })

    if patient.smoke == 1:
        add("smoke")

    if patient.gluc == 3:
        add("gluc")

    if patient.alco == 1:
        add("alco")

    if patient.active == 0:
        add("active")

    return factors

def build_clinical_factors(flags, lang):
    clinical_factors = []
    direction_key = "increases"
    for flag in flags:
        loc = t(lang, "clinical_factors", flag)
        if not loc:
            continue

        clinical_factors.append({
            "key": flag,
            "factor": loc["name"],
            "direction": direction_key,
            "clinical_note": loc["note"]
        })

    return clinical_factors

def build_clinical_conditions(flags, lang):
    conditions = []

    for flag in flags:
        loc = t(lang, "clinical_conditions", flag)
        if not loc:
            continue

        conditions.append({
            "key": flag,
            "condition": loc["name"],
            "severity": loc["severity"],
            "note": loc["note"]
        })

    return conditions    


def evaluate_clinical_risk(
    patient,
    model,
    shap_explainer,
    lang: str
) -> dict:
    """
    Central clinical decision pipeline.
    Returns full clinical-grade result.
    """
    from app.model_loader import get_model_performance_metrics
    
    model_metrics = get_model_performance_metrics()
    FEATURE_COLUMNS = [
    "index",
    "age",
    "gender",
    "height", 
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active",
    "age_years",
    "bmi"
    ]

    # Compute derived features
    age_days = patient.age_years * 365  # approximate
    height_cm = 170  # dummy value
    weight_kg = patient.bmi * (height_cm / 100) ** 2  # compute weight from bmi

    patient_df = pd.DataFrame([{
        "index": 0,
        "age": age_days,
        "gender": patient.gender,
        "height": height_cm,
        "weight": weight_kg,
        "ap_hi": patient.ap_hi,
        "ap_lo": patient.ap_lo,
        "cholesterol": patient.cholesterol,
        "gluc": patient.gluc,
        "smoke": patient.smoke,
        "alco": patient.alco,
        "active": patient.active,
        "age_years": patient.age_years,
        "bmi": patient.bmi
    }])

    
    # 1. Предсказываем риск
    risk_proba = float(model.predict_proba(patient_df)[0, 1])

    # 2. Категория риска
    risk_category = categorize_risk(risk_proba)

    # 3. Confidence & uncertainty layer
    confidence = assess_prediction_confidence(risk_proba)
    confidence_block = t(lang, "confidence", confidence["confidence_level"])
    confidence_title = confidence_block["title"]
    confidence_note = confidence_block["note"]

    # 4. Safety warnings
    safety_warnings = collect_safety_warnings(
        patient,
        confidence["confidence_level"],
        lang
    )
    
    # 5. SHAP-based explanation 
    shap_values = explain_patient(shap_explainer, patient_df)
    # 6. Клиническое объяснение
    # 6.1. SHAP факторы
    clinical_explanation = interpret_shap(
        shap_values=shap_values,
        patient_data=patient,
        lang=lang,
        model_metrics=model_metrics
    )
    existing_keys = {item["key"] for item in clinical_explanation}
    
    # 6.2. Поведенческие факторы
    # Rule-based (clinical) factors
    rule_factors = collect_clinical_risk_factors(patient, lang)
    for item in rule_factors:
        if item["key"] not in existing_keys:
            clinical_explanation.append(item)
            existing_keys.add(item["key"])
          
    # 6.3. Пороговые клинические флаги
    flags = collect_rule_based_flags(patient)
    clinical_rule_factors = build_clinical_factors(flags, lang)
    
    for item in clinical_rule_factors:
        if item["key"] not in existing_keys:
            clinical_explanation.append(item)
            existing_keys.add(item["key"])
    
    # 6.4. Клинические состояния
    clinical_conditions = build_clinical_conditions(flags, lang)
    for condition in clinical_conditions:
        key = condition["key"]

        if key not in existing_keys:
            clinical_explanation.insert(0, {
                "key": key,
                "factor": condition["condition"],
                "direction": "increases",
                "clinical_note": condition["note"]
            })
            existing_keys.add(key)
            
    clinical_explanation.sort(
    key=lambda x: CLINICAL_PRIORITY.get(x["key"], 99)
    )
    # 7. Risk card
    risk_card = build_risk_card(
        lang=lang,
        risk_probability=risk_proba,
        risk_category=risk_category,
        confidence_level=confidence["confidence_level"],
        confidence_note=confidence_note,
        clinical_explanation=clinical_explanation
    )
    
    for item in clinical_explanation:
        item["direction"] = LOCALIZATION[lang]["directions"].get(
            item["direction"],
            item["direction"]
        )  

    # 8. Финальный clinical-grade JSON
    return {
        "risk_probability": round(risk_proba, 3),
        "risk_category": risk_category,
        "risk_label": t(lang, "risk_category", risk_category),

        "confidence_level": confidence["confidence_level"],
        "confidence_title": confidence_title,
        "confidence_note": confidence_note,
        
        "clinical_explanation": clinical_explanation,
        "clinical_conditions": clinical_conditions,
        
        "risk_card": risk_card,
        
        "safety_warnings": safety_warnings,
        "disclaimer": t(lang, "disclaimer", None),
        "audit": build_audit_block(),
        "performance_metrics": get_model_performance_metrics()
    }
