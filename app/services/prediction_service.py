"""
Сервисный слой для предсказаний риска
"""
from app.schemas import PatientInput, PredictionResponse
from app.risk_logic import evaluate_clinical_risk
from app.core.logging import logger


class PredictionService:
    """Сервис для обработки предсказаний сердечно-сосудистого риска"""
    
    def __init__(self, model, shap_explainer, model_metrics=None):
        self.model = model
        self.shap_explainer = shap_explainer
        self.model_metrics = model_metrics
    
    async def predict(self, patient: PatientInput) -> PredictionResponse:
        """
        Основной метод для предсказания риска
        
        Args:
            patient: Входные данные пациента
            
        Returns:
            PredictionResponse: Полный ответ с предсказанием и клиническими данными
        """
        lang = getattr(patient, "ui_language", "en")
        
        logger.info(
            f"Processing prediction request for patient: "
            f"age={patient.age_years}, gender={patient.gender}"
        )
        
        try:
            result = evaluate_clinical_risk(
                patient=patient,
                model=self.model,
                shap_explainer=self.shap_explainer,
                lang=lang,
                model_metrics=self.model_metrics
            )
            
            logger.info(
                f"Prediction completed: risk={result.risk_category}, "
                f"probability={result.risk_probability:.3f}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}", exc_info=True)
            raise


