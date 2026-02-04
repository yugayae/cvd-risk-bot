# Предложения по улучшению архитектуры проекта

## 📁 Структура разделения frontend скрипта

### Рекомендуемая структура модулей:

```
frontend/
├── js/
│   ├── constants.js          # Все константы и тексты
│   ├── validation.js         # Валидация данных
│   ├── api.js                # API запросы
│   ├── render/
│   │   ├── patient-report.js # Рендеринг отчета для пациента
│   │   ├── doctor-report.js  # Рендеринг отчета для врача
│   │   └── safety-warnings.js # Рендеринг предупреждений
│   ├── utils/
│   │   ├── normalization.js  # Нормализация данных
│   │   ├── form-handlers.js  # Обработчики формы
│   │   └── localization.js  # Локализация
│   └── main.js               # Главный файл, инициализация
├── index.html
└── styles.css
```

### Преимущества:
- ✅ Модульность и переиспользование
- ✅ Легче тестировать отдельные компоненты
- ✅ Проще поддерживать и расширять
- ✅ Возможность lazy loading модулей
- ✅ Четкое разделение ответственности

### Пример использования ES6 модулей:

```javascript
// main.js
import { validatePatientData } from './js/validation.js';
import { fetchPrediction } from './js/api.js';
import { renderPatientResult } from './js/render/patient-report.js';
import { renderDoctorReport } from './js/render/doctor-report.js';

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});
```

---

## 🔧 Предложения по улучшению бэкенда

### 1. Структура проекта

```
app/
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predictions.py    # Эндпоинты для предсказаний
│   │   └── health.py         # Health check эндпоинты
│   └── dependencies.py        # Зависимости (модель, explainer)
├── core/
│   ├── __init__.py
│   ├── config.py              # Конфигурация приложения
│   └── exceptions.py          # Кастомные исключения
├── services/
│   ├── __init__.py
│   ├── prediction_service.py  # Бизнес-логика предсказаний
│   └── validation_service.py  # Валидация данных
├── models/                    # ML модели и explainers
├── schemas/                   # Pydantic схемы
├── utils/                     # Утилиты
└── main.py                    # Точка входа
```

### 2. Улучшения кода

#### a) Конфигурация через переменные окружения

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: str = "model/primary_care_cvd_risk_model.pkl"
    shap_background_path: str = "model/shap_background.csv"
    api_version: str = "1.0.0"
    log_level: str = "INFO"
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### b) Dependency Injection для модели

```python
# app/api/dependencies.py
from fastapi import Depends
from app.model_loader import load_model
from app.shap_explainer import create_shap_explainer

_model = None
_explainer = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model

def get_explainer():
    global _explainer
    if _explainer is None:
        _explainer = create_shap_explainer(get_model())
    return _explainer
```

#### c) Сервисный слой

```python
# app/services/prediction_service.py
from app.schemas import PatientInput, PredictionResponse
from app.risk_logic import evaluate_clinical_risk

class PredictionService:
    def __init__(self, model, explainer):
        self.model = model
        self.explainer = explainer
    
    async def predict(self, patient: PatientInput) -> PredictionResponse:
        """Основной метод для предсказания риска"""
        lang = getattr(patient, "ui_language", "en")
        
        return evaluate_clinical_risk(
            patient=patient,
            model=self.model,
            shap_explainer=self.explainer,
            lang=lang
        )
```

#### d) Улучшенные эндпоинты

```python
# app/api/routes/predictions.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_model, get_explainer
from app.services.prediction_service import PredictionService
from app.schemas import PatientInput, PredictionResponse
from app.core.exceptions import ValidationError

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("", response_model=PredictionResponse)
async def predict_risk(
    patient: PatientInput,
    model = Depends(get_model),
    explainer = Depends(get_explainer)
):
    """
    Предсказание сердечно-сосудистого риска
    
    - **age_years**: Возраст пациента (18-90)
    - **ap_hi**: Систолическое АД (90-220)
    - **ap_lo**: Диастолическое АД (50-140)
    - И другие параметры...
    """
    try:
        service = PredictionService(model, explainer)
        return await service.predict(patient)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

#### e) Логирование

```python
# app/core/logging.py
import logging
from app.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

#### f) Обработка ошибок

```python
# app/core/exceptions.py
class CVDRiskException(Exception):
    """Базовое исключение для приложения"""
    pass

class ValidationError(CVDRiskException):
    """Ошибка валидации данных"""
    pass

class ModelError(CVDRiskException):
    """Ошибка при работе с моделью"""
    pass
```

#### g) Middleware для логирования запросов

```python
# app/main.py
from fastapi import Request
import time
from app.core.logging import logger

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    return response
```

### 3. Тестирование

```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_valid_data():
    payload = {
        "age_years": 50,
        "ap_hi": 120,
        "ap_lo": 80,
        # ... другие поля
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "risk_probability" in response.json()
```

### 4. Документация API

- ✅ Автоматическая документация через FastAPI (Swagger/ReDoc)
- ✅ Добавить примеры запросов/ответов
- ✅ Описание всех полей и ограничений

### 5. Безопасность

- ✅ Валидация входных данных (уже есть через Pydantic)
- ✅ Rate limiting для API
- ✅ CORS настройки для production
- ✅ Логирование подозрительных запросов

### 6. Производительность

- ✅ Кэширование модели (уже реализовано)
- ✅ Асинхронная обработка (FastAPI поддерживает)
- ✅ Оптимизация SHAP вычислений
- ✅ Connection pooling для БД (если будет добавлена)

### 7. Мониторинг

```python
# app/core/metrics.py
from prometheus_client import Counter, Histogram

prediction_counter = Counter(
    'predictions_total',
    'Total number of predictions',
    ['status']
)

prediction_duration = Histogram(
    'prediction_duration_seconds',
    'Time spent processing predictions'
)
```

### 8. Дополнительные эндпоинты

```python
# GET /api/v1/model/info - информация о модели
# GET /api/v1/model/version - версия модели
# POST /api/v1/batch/predict - батч предсказания
# GET /api/v1/stats - статистика использования
```

---

## 📦 Дополнительные улучшения

### Frontend:
- ✅ Добавить loading states
- ✅ Добавить error boundaries
- ✅ Оптимизация bundle size (tree shaking)
- ✅ Service Worker для offline работы
- ✅ Accessibility (ARIA labels)

### Backend:
- ✅ Docker контейнеризация
- ✅ CI/CD pipeline
- ✅ Database для хранения истории предсказаний (опционально)
- ✅ Аутентификация для production (если нужно)
- ✅ Версионирование API (/api/v1/, /api/v2/)

---

## 🚀 Приоритеты внедрения

1. **Высокий приоритет:**
   - Разделение frontend скрипта на модули
   - Улучшение структуры бэкенда (сервисный слой)
   - Логирование и обработка ошибок
   - Тестирование основных эндпоинтов

2. **Средний приоритет:**
   - Конфигурация через .env
   - Дополнительные эндпоинты
   - Мониторинг и метрики

3. **Низкий приоритет:**
   - Docker
   - CI/CD
   - Database интеграция

