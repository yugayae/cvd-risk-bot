from pydantic import BaseModel, Field
from typing import List
from typing import Literal
from pydantic import BaseModel, ConfigDict

# -------------------------
# ВХОДНЫЕ ДАННЫЕ ПАЦИЕНТА
# -------------------------

class PatientInput(BaseModel):
    age_years: int = Field(..., ge=18, le=90, description="Возраст пациента (годы)")
    ap_hi: int = Field(..., ge=90, le=220, description="Систолическое АД (мм рт.ст.)")
    ap_lo: int = Field(..., ge=50, le=140, description="Диастолическое АД (мм рт.ст.)")
    cholesterol: int = Field(..., ge=1, le=3, description="Холестерин: 1-норма, 2-повышен, 3-высокий")
    bmi: float = Field(..., ge=15, le=60, description="ИМТ")
    active: int = Field(..., ge=0, le=1, description="Физическая активность (0/1)")
    smoke: int = Field(..., ge=0, le=1, description="Smoking status")
    alco: int = Field(..., ge=0, le=1, description="Alcohol intake")
    gluc: int = Field(..., ge=1, le=3, description="Glucose level")
    gender: int = Field(..., ge=1, le=2, description="1-female, 2-male")
    ui_language: Literal["en", "ru", "kr"] = "en"

# -------------------------
# ОБЪЯСНЕНИЕ РИСКА
# -------------------------

class RiskFactor(BaseModel):
    feature: str
    effect: str
    clinical_note: str

class ClinicalExplanationItem(BaseModel):
    factor: str
    direction: str
    clinical_note: str

class ClinicalConditionItem(BaseModel):
    key: str
    condition: str
    severity: str
    note: str

# -------------------------
# ВЫХОД ДЛЯ ВРАЧА
# -------------------------
class AuditInfo(BaseModel):
    timestamp: str
    model_version: str
    request_id: str
    api_version: str
    
    model_config = ConfigDict(
        protected_namespaces=()
    )

class ModelPerformanceMetrics(BaseModel):
    sensitivity: float
    specificity: float
    ppv: float
    npv: float
    pr_auc: float
    roc_auc: float
    brier_score: float
    precision: float
    recall: float
    f1_score: float
    gender_specific_roc_auc: dict

class PredictionResponse(BaseModel):
    risk_probability: float
    risk_category: Literal["low", "moderate", "high"]
    risk_label: str

    confidence_level: Literal["low", "moderate", "high"]
    confidence_title: str
    confidence_note: str

    clinical_explanation: List[ClinicalExplanationItem]
    clinical_conditions: List[ClinicalConditionItem]

    safety_warnings: List[str]

    risk_card: dict
    disclaimer: str
    audit: AuditInfo
    performance_metrics: ModelPerformanceMetrics
    data_validation: dict

