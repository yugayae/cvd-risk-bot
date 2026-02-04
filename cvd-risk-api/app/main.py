from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import pandas as pd

from app.schemas import PatientInput, PredictionResponse
from app.model_loader import load_model
from app.risk_logic import (
    categorize_risk,
    assess_prediction_confidence
)
from app.shap_explainer import (
    create_shap_explainer,
    explain_patient,
)

from app.risk_card import build_risk_card
from app.safety import collect_safety_warnings
from app.localization import t
from .shap_interpreter import interpret_shap
from app.risk_logic import (
    categorize_risk,
    assess_prediction_confidence,
    collect_clinical_risk_factors,
    build_clinical_factors,
    collect_rule_based_flags,
    build_clinical_conditions   
)
from app.risk_logic import evaluate_clinical_risk

app = FastAPI(
    title="CVD Risk API",
    description="Clinical-grade cardiovascular risk assessment",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()
shap_explainer = create_shap_explainer(model)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/metrics")
def get_metrics():
    return get_model_performance_metrics()


@app.post("/predict", response_model=PredictionResponse)
def predict_risk(patient_data: dict):

    # Попытка валидации
    try:
        patient = PatientInput(**patient_data)
        is_valid = True
        validation_errors = []
    except Exception as e:
        # Если валидация не прошла, создаем объект с defaults, но отмечаем невалидность
        patient = PatientInput(**{k: v for k, v in patient_data.items() if k in PatientInput.__fields__})
        is_valid = False
        validation_errors = str(e)

    lang = getattr(patient, "ui_language", "ru")

    result = evaluate_clinical_risk(
        patient=patient,
        model=model,
        shap_explainer=shap_explainer,
        lang=lang
    )
    
    # Добавляем информацию о валидации в результат
    result['data_validation'] = {
        'is_valid': is_valid,
        'errors': validation_errors
    }
    
    # Добавляем предупреждение в safety_warnings если данные невалидны
    if not is_valid:
        warning_text = {
            'en': 'Input data validation failed. Results calculated but interpret with caution.',
            'ru': 'Валидация входных данных не пройдена. Результаты рассчитаны, но интерпретируйте с осторожностью.',
            'kr': '입력 데이터 검증에 실패했습니다. 결과가 계산되었지만 신중하게 해석하세요.'
        }.get(lang, warning_text['en'])
        if 'safety_warnings' not in result:
            result['safety_warnings'] = []
        result['safety_warnings'].append(warning_text)
    
    return result
    

