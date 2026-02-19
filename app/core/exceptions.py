"""
Кастомные исключения для приложения
"""


class CVDRiskException(Exception):
    """Базовое исключение для приложения CVD Risk"""
    pass


class ValidationError(CVDRiskException):
    """Ошибка валидации входных данных"""
    pass


class ModelError(CVDRiskException):
    """Ошибка при работе с ML моделью"""
    pass


class DataProcessingError(CVDRiskException):
    """Ошибка при обработке данных"""
    pass


