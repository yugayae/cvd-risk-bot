"""
Dependencies для FastAPI эндпоинтов
"""
from functools import lru_cache
from app.model_loader import load_model
from app.shap_explainer import create_shap_explainer
from app.core.config import settings


@lru_cache()
def get_model():
    """
    Загружает и кэширует ML модель
    Использует LRU cache для предотвращения повторной загрузки
    """
    return load_model()


@lru_cache()
def get_shap_explainer():
    """
    Создает и кэширует SHAP explainer
    """
    model = get_model()
    return create_shap_explainer(model)


