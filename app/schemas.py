from pydantic import BaseModel, Field, model_validator
from typing import List
from typing import Literal
from pydantic import BaseModel, ConfigDict

# -------------------------
# ВХОДНЫЕ ДАННЫЕ ПАЦИЕНТА
# -------------------------

class PatientInput(BaseModel):
    age_years: int = Field(..., ge=18, le=90, description="Возраст пациента (годы)")
    height: float = Field(..., ge=100, le=250, description="Рост (см)")
    weight: float = Field(..., ge=30, le=250, description="Вес (кг)")
    bmi: float | None = Field(None, description="ИМТ (рассчитывается автоматически)")
    ap_hi: int = Field(..., ge=60, le=240, description="Систолическое АД (мм рт.ст.)")
    ap_lo: int = Field(..., ge=40, le=160, description="Диастолическое АД (мм рт.ст.)")
    cholesterol: int = Field(..., ge=1, le=3, description="Холестерин: 1-норма, 2-повышен, 3-высокий")
    active: int = Field(..., ge=0, le=1, description="Физическая активность (0/1)")
    smoke: int = Field(..., ge=0, le=1, description="Smoking status")
    alco: int = Field(..., ge=0, le=1, description="Alcohol intake")
    gluc: int = Field(..., ge=1, le=3, description="Glucose level")
    gender: int = Field(..., ge=1, le=2, description="1-female, 2-male")
    ui_language: Literal["en", "ru", "kr"] = "en"
    region: str | None = Field("Unknown", description="WHO Region Code (AFR, AMR, SEAR, EUR, EMR, WPR)")

    @model_validator(mode='after')
    def validate_clinical_data(self):
        # 1. Check BP
        if self.ap_hi <= self.ap_lo:
            raise ValueError("Systolic pressure (ap_hi) must be higher than diastolic (ap_lo)")

        # 2. Calculate BMI if not set
        if self.bmi is None and self.weight and self.height:
            height_m = self.height / 100.0
            self.bmi = round(self.weight / (height_m * height_m), 2)
        
        return self

# -------------------------
# ОБЪЯСНЕНИЕ РИСКА
# -------------------------

class RiskFactor(BaseModel):
    feature: str
    effect: str
    clinical_note: str

class ClinicalExplanationItem(BaseModel):
    key: str
    factor: str
    direction: str
    raw_direction: str
    shap_value: float | None = None
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
    sensitivity: float | None = None
    specificity: float | None = None
    ppv: float | None = None
    npv: float | None = None
    pr_auc: float | None = None
    roc_auc: float | None = None
    brier_score: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1_score: float | str | None = None
    gender_specific_roc_auc: dict | None = None

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
    patient_bmi: float | None = None

    risk_card: dict
    disclaimer: str
    audit: AuditInfo
    performance_metrics: ModelPerformanceMetrics
    data_validation: dict

