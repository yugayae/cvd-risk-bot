import numpy as np
from localization import LOCALIZATION
from clinical_expectations import CLINICAL_FACTOR_RISK

CLINICAL_ONLY_FEATURES = {
    "cholesterol"
}

def interpret_shap(
    shap_values,
    patient_data,
    lang: str,
    model_metrics: dict = None,
    threshold: float = 0.05
):
    """
    Преобразует SHAP значения в клинически интерпретируемые факторы
    """

    if hasattr(shap_values, "values") and hasattr(shap_values, "feature_names"):
        values = shap_values.values

        # ✅ CASE 1: (1, n_features, 2) → берём пациента 0, класс 1
        if isinstance(values, np.ndarray) and values.ndim == 3:
            values = values[0, :, 1]

        # ✅ CASE 2: (n_features, 2)
        elif isinstance(values, np.ndarray) and values.ndim == 2:
            values = values[:, 1]

        # ✅ CASE 3: (n_features,)
        elif isinstance(values, np.ndarray) and values.ndim == 1:
            values = values

        else:
            raise ValueError("Unsupported SHAP values shape")

        shap_dict = {
            feature: float(value)
            for feature, value in zip(
                shap_values.feature_names,
                values
            )
        }

    else:
        shap_dict = shap_values

    explanations = []

    # Бинарные признаки, которые требуют специальной обработки
    BINARY_FEATURES = {"smoke", "alco", "active"}
    
    for feature, shap_value in shap_dict.items():
        if feature in CLINICAL_ONLY_FEATURES:
            continue

        # Получаем значение признака у пациента
        patient_feature_value = getattr(patient_data, feature, None)
        
        # Обязательные факторы риска - всегда включаем независимо от SHAP threshold
        is_mandatory_risk = (
            (feature in {"smoke", "alco"} and patient_feature_value == 1) or
            (feature == "gluc" and patient_feature_value and patient_feature_value > 1)
        )
        
        if not is_mandatory_risk and abs(shap_value) < threshold:
            continue

        feature_loc = LOCALIZATION[lang]["shap_factors"].get(feature)
        if not feature_loc:
            continue
        
        # Специальная обработка для факторов, которые ВСЕГДА являются risk factors
        if feature in {"smoke", "alco"} and patient_feature_value == 1:
            # Курение и алкоголь ВСЕГДА увеличивают риск, когда присутствуют
            ml_direction = "increases"
        elif feature == "gluc" and patient_feature_value and patient_feature_value > 1:
            # Высокий уровень глюкозы ВСЕГДА увеличивает риск
            ml_direction = "increases"
        elif feature == "active" and patient_feature_value == 1:
            # Физическая активность может быть protective, НО не может полностью перекрывать risk factors
            # Используем SHAP значение, но ограничиваем protective эффект
            if shap_value < 0:  # SHAP показывает снижение риска
                ml_direction = "reduces"
            else:
                # Если SHAP не показывает снижение, или даже показывает увеличение,
                # для активных пациентов всё равно считаем как protective, но слабее
                ml_direction = "reduces"
        elif feature == "active" and patient_feature_value == 0:
            # Отсутствие активности увеличивает риск
            ml_direction = "increases"
        elif feature in BINARY_FEATURES and patient_feature_value is not None:
            # Остальные бинарные признаки
            if feature in {"smoke", "alco"}:
                # Для smoke/alco=0 (отсутствие) - снижает риск относительно наличия
                ml_direction = "reduces" if patient_feature_value == 0 else "increases"
            else:
                ml_direction = "increases" if shap_value > 0 else "reduces"
        else:
            # Для непрерывных признаков используем стандартную интерпретацию
            ml_direction = "increases" if shap_value > 0 else "reduces"

        # Клиническое ожидание
        clinical_expectation = CLINICAL_FACTOR_RISK.get(feature)

        # Согласование ML и медицины
        # Если ML показывает противоположное клиническому ожиданию, приоритет клинике
        if clinical_expectation == "increases" and ml_direction == "reduces":
            direction_key = "increases"
            clinical_note = feature_loc["note"]
        elif clinical_expectation == "reduces" and ml_direction == "increases":
            direction_key = "reduces"
            clinical_note = feature_loc["note"]
        else:
            direction_key = ml_direction
            clinical_note = feature_loc["note"]

        explanations.append({
            "key": feature,
            "factor": feature_loc["name"],
            "direction": direction_key,
            "clinical_note": clinical_note
        })

    # Add metric-based interpretation warnings
    if model_metrics:
        precision = model_metrics.get('precision', 0.5)
        roc_auc = model_metrics.get('roc_auc', 0.8)
        
        # If precision is low, add warning about potential false positives
        if precision < 0.6:
            for exp in explanations:
                if exp['direction'] == 'increases':
                    exp['clinical_note'] += f" {LOCALIZATION[lang]['metric_warnings'].get('low_precision', 'Note: Model has moderate precision, consider additional clinical evaluation.')}"
                    break  # Add to first increasing factor
        
        # If ROC-AUC is moderate, add general caution
        if roc_auc < 0.8:
            for exp in explanations:
                exp['clinical_note'] += f" {LOCALIZATION[lang]['metric_warnings'].get('moderate_discrimination', 'Model discrimination is moderate, interpret results cautiously.')}"
                break  # Add to first factor

    return explanations
