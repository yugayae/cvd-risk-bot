"""
Настройка логирования для приложения
"""
import logging
import sys
from app.core.config import settings


def setup_logging():
    """Настраивает логирование для приложения"""
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Уменьшаем уровень логирования для некоторых библиотек
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)


# Инициализация при импорте
setup_logging()

# Создаем логгер для использования в приложении
logger = logging.getLogger(__name__)


