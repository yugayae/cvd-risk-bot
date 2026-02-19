"""
Улучшенная версия main.py с новой архитектурой
Это пример того, как можно рефакторить текущий main.py
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import CVDRiskException, ValidationError, ModelError
from app.api.dependencies import get_model, get_shap_explainer
from app.services.prediction_service import PredictionService
from app.schemas import PatientInput, PredictionResponse


# Инициализация приложения
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирует все HTTP запросы"""
    start_time = time.time()
    
    # Пропускаем запрос
    response = await call_next(request)
    
    # Вычисляем время обработки
    process_time = time.time() - start_time
    
    # Логируем
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    # Добавляем заголовок с временем обработки
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Обработчик исключений
@app.exception_handler(CVDRiskException)
async def cvd_exception_handler(request: Request, exc: CVDRiskException):
    """Обработчик кастомных исключений"""
    logger.error(f"CVDRiskException: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "type": exc.__class__.__name__}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик общих исключений"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "InternalError"}
    )


# Health check
@app.get("/")
@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {
        "status": "ok",
        "version": settings.api_version,
        "service": "CVD Risk API"
    }


# Основной эндпоинт для предсказаний
@app.post("/predict", response_model=PredictionResponse)
async def predict_risk(
    patient: PatientInput,
    model = None,  # Будет инжектиться через Depends
    explainer = None  # Будет инжектиться через Depends
):
    """
    Предсказание сердечно-сосудистого риска
    
    Принимает данные пациента и возвращает:
    - Вероятность риска
    - Категорию риска (low/moderate/high)
    - Уровень уверенности модели
    - Клиническое объяснение факторов риска
    - Предупреждения о безопасности
    
    **Параметры:**
    - **age_years**: Возраст пациента (18-90 лет)
    - **ap_hi**: Систолическое артериальное давление (90-220 mmHg)
    - **ap_lo**: Диастолическое артериальное давление (50-140 mmHg)
    - **cholesterol**: Уровень холестерина (1=норма, 2=повышен, 3=высокий)
    - **bmi**: Индекс массы тела (15-60)
    - **active**: Физическая активность (0=нет, 1=да)
    - **smoke**: Курение (0=нет, 1=да)
    - **alco**: Употребление алкоголя (0=нет, 1=да)
    - **gluc**: Уровень глюкозы (1=норма, 2=повышен, 3=высокий)
    - **gender**: Пол (1=женский, 2=мужской)
    - **ui_language**: Язык интерфейса (en/ru/kr)
    """
    # Получаем зависимости если не переданы
    if model is None:
        model = get_model()
    if explainer is None:
        explainer = get_shap_explainer()
    
    # Создаем сервис и выполняем предсказание
    service = PredictionService(model, explainer)
    return await service.predict(patient)


# Дополнительные эндпоинты (опционально)
@app.get("/api/v1/model/info")
async def get_model_info():
    """Информация о модели"""
    return {
        "version": settings.api_version,
        "model_path": settings.model_path,
        "description": "Primary Care CVD Risk Model"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_improved:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


