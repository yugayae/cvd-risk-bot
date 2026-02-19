"""
Конфигурация приложения через переменные окружения
"""
from pydantic_settings import BaseSettings  # pyright: ignore[reportMissingImports]
from typing import List


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Пути к моделям
    model_path: str = "model/calibrated_catboost.pkl"
    shap_background_path: str = "model/shap_background_catboost_clean.csv"
    
    # API настройки
    api_version: str = "1.0.0"
    api_title: str = "CVD Risk API"
    api_description: str = "Clinical-grade cardiovascular risk assessment"
    
    # Логирование
    log_level: str = "INFO"
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Производительность
    max_request_size: int = 1024 * 1024  # 1MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()


