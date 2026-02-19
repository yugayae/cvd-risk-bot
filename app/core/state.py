from app.model_loader import load_model, get_model_performance_metrics
from app.shap_explainer import create_shap_explainer

class AppState:
    model = None
    shap_explainer = None
    model_metrics = None
    
    @classmethod
    def initialize(cls):
        if cls.model is None:
            cls.model = load_model()
            cls.shap_explainer = create_shap_explainer(cls.model)
            cls.model_metrics = get_model_performance_metrics()

global_state = AppState
