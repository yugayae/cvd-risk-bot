import shap
import pandas as pd
from pathlib import Path
from catboost import CatBoostClassifier


BACKGROUND_PATH = Path("model/shap_background_catboost_clean.csv")


def load_background_data():
    """Загружает background данные для SHAP объяснений"""
    if not BACKGROUND_PATH.exists():
        raise FileNotFoundError(
            f"SHAP background data not found at {BACKGROUND_PATH.resolve()}"
        )
    df = pd.read_csv(BACKGROUND_PATH)
    
    # Выбираем только релевантные признаки для модели
    relevant_features = [
        'index', 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
        'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'age_years', 'bmi'
    ]
    
    # Проверяем, что все необходимые признаки присутствуют
    missing_features = [f for f in relevant_features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Missing features in background data: {missing_features}")
    
    return df[relevant_features]


def create_shap_explainer(model):
    """
    Создает оптимизированный SHAP explainer для CatBoost модели.
    
    Для CatBoost используется TreeExplainer, который:
    - Работает намного быстрее, чем общий Explainer
    - Требует меньше памяти
    - Дает более точные объяснения для tree-based моделей
    
    Args:
        model: Обученная CatBoost модель (может быть обернута в CalibratedClassifierCV)
        
    Returns:
        SHAP TreeExplainer для CatBoost модели
    """
    # Получаем базовую модель (может быть обернута в CalibratedClassifierCV)
    base_model = model
    if hasattr(model, 'base_estimator'):
        # Если модель обернута в CalibratedClassifierCV
        base_model = model.base_estimator
    elif hasattr(model, 'estimator'):
        # Альтернативный способ получения базовой модели
        base_model = model.estimator
    
    # Проверяем, что это CatBoost модель
    is_catboost = (
        isinstance(base_model, CatBoostClassifier) or
        hasattr(base_model, '__class__') and 'CatBoost' in str(base_model.__class__)
    )
    
    if not is_catboost:
        # Fallback для других типов моделей
        background_df = load_background_data()
        explainer = shap.Explainer(
            lambda x: model.predict_proba(
                pd.DataFrame(x, columns=background_df.columns)
            ),
            background_df.values
        )
        return explainer
    
    # Оптимизированный TreeExplainer для CatBoost
    # TreeExplainer работает напрямую с деревьями, но может иметь проблемы с совместимостью
    # Используем общий Explainer с prediction function для надежности
    background_df = load_background_data()
    
    # Используем общий Explainer с lambda функцией для предсказаний
    explainer = shap.Explainer(
        lambda x: base_model.predict_proba(
            pd.DataFrame(x, columns=background_df.columns).astype({
                'index': 'int64',
                'age': 'int64', 
                'gender': 'int64',
                'height': 'int64',
                'weight': 'float64',
                'ap_hi': 'int64',
                'ap_lo': 'int64',
                'cholesterol': 'int64',
                'gluc': 'int64',
                'smoke': 'int64',
                'alco': 'int64',
                'active': 'int64',
                'age_years': 'int64',
                'bmi': 'float64'
            })
        ),
        background_df.values,
        feature_names=background_df.columns.tolist()
    )
    
    return explainer


def explain_patient(explainer, patient_df: pd.DataFrame):
    """
    Генерирует SHAP значения для данных пациента.
    
    Работает как с TreeExplainer (для CatBoost), так и с обычным Explainer.
    TreeExplainer возвращает те же объекты SHAP, что и обычный Explainer,
    поэтому интерфейс остается совместимым.
    
    Args:
        explainer: SHAP explainer (TreeExplainer или Explainer)
        patient_df: DataFrame с данными пациента
        
    Returns:
        SHAP Explanation объект с значениями для каждого признака
    """
    return explainer(patient_df)

FEATURE_LABELS = {
    "ap_hi": "Systolic blood pressure",
    "ap_lo": "Diastolic blood pressure",
    "cholesterol": "Cholesterol level",
    "bmi": "Body mass index",
    "age_years": "Age",
    "gluc": "Blood glucose level",
    "smoke": "Smoking status",
    "alco": "Alcohol intake",
    "active": "Physical activity",
    "gender": "Sex"
}

def shap_to_clinical_text(shap_values, patient_df, top_n=3):

    # берём SHAP значения для класса "1" (высокий риск)
    values = shap_values.values[0][:, 1]
    features = patient_df.columns

    explanation = []

    for feature, value in sorted(
        zip(features, values),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:top_n]:

        clinical_name = FEATURE_LABELS.get(feature, feature)
        
        explanation.append({
            "feature": clinical_name,
            "effect": "increases risk" if value > 0 else "reduces risk",
            "relative_impact": round(float(value), 3)
        })

    return explanation

from app.clinical_mapping import CLINICAL_EXPLANATIONS


def build_clinical_explanation(shap_factors):
    explanation = []

    for item in shap_factors:
        feature = item["feature"]

        explanation.append({
            "factor": feature,
            "direction": item["effect"],
            "clinical_note": CLINICAL_EXPLANATIONS.get(
                feature,
                "This factor contributes to cardiovascular risk"
            )
        })

    return explanation