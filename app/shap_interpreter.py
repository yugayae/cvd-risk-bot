import numpy as np
from .localization import LOCALIZATION
from .clinical_expectations import CLINICAL_FACTOR_RISK

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
    Преобразует SHAP значения в клин. интерпретируемые факторы.
    Приоритет отдается медицинской логике (патологическим порогам).
    """

    if hasattr(shap_values, "values") and hasattr(shap_values, "feature_names"):
        values = shap_values.values
        if isinstance(values, np.ndarray) and values.ndim == 3:
            values = values[0, :, 1]
        elif isinstance(values, np.ndarray) and values.ndim == 2:
            values = values[:, 1]
        elif isinstance(values, np.ndarray) and values.ndim == 1:
            values = values
        else:
            raise ValueError(f"Unsupported SHAP values shape: {values.shape}")

        shap_dict = {
            feature: float(value)
            for feature, value in zip(shap_values.feature_names, values)
        }
    else:
        shap_dict = shap_values

    explanations = []

    for feature, shap_value in shap_dict.items():
        if feature in CLINICAL_ONLY_FEATURES:
            continue

        if feature == "age":
            # Map 'age' feature (usually days) to patient data
            val = getattr(patient_data, "age_years", None)
            if val is not None:
                val = val * 365.25 # Convert to days for pathological check
        else:
            val = getattr(patient_data, feature, None)
        
        # 1. Принудительные патологические пороги (Medical Ground Truth)
        is_pathological = False
        if feature == "ap_hi" and val is not None and val >= 140: is_pathological = True
        elif feature == "ap_lo" and val is not None and val >= 90: is_pathological = True
        elif feature == "gluc" and val is not None and val > 1: is_pathological = True
        elif feature == "smoke" and val == 1: is_pathological = True
        elif feature == "alco" and val == 1: is_pathological = True
        elif feature == "active" and val == 0: is_pathological = True
        elif feature == "bmi" and val is not None and val >= 30: is_pathological = True
        elif feature == "age" and val is not None and val >= 21900: is_pathological = True # 60 years * 365

        # 2. Фильтрация
        # Важные факторы (патология или сильное влияние) оставляем
        if not is_pathological and abs(shap_value) < threshold:
            continue

        feature_loc = LOCALIZATION[lang]["shap_factors"].get(feature)
        if not feature_loc:
            continue
        
        # 3. Базовая логика направления
        ml_direction = "increases" if shap_value > 0 else "reduces"

        # 4. Клиническая коррекция (Медицинский здравый смысл)
        if is_pathological:
            direction_key = "increases"
        elif feature == "active" and val == 1:
            # Если человек активен, это ВСЕГДА снижает риск (даже если SHAP говорит обратное)
            direction_key = "reduces"
        elif feature in {"smoke", "alco", "gluc"} and (val is None or val <= 1 or val == 0):
            # Если фактора нет, он точно не повышает риск
            direction_key = "reduces"
        else:
            # Проверка по CLINICAL_FACTOR_RISK для пограничных значений
            clinical_exp = CLINICAL_FACTOR_RISK.get(feature)
            if clinical_exp == "increases" and val is not None:
                if feature == "ap_hi": direction_key = "increases" if val >= 135 else "reduces"
                elif feature == "ap_lo": direction_key = "increases" if val >= 85 else "reduces"
                elif feature == "age": direction_key = "increases" if val >= 55 else "reduces"
                elif feature == "bmi": direction_key = "increases" if val >= 25 else "reduces"
                else: direction_key = ml_direction
            else:
                direction_key = ml_direction

        # 5. Синхронизация значения SHAP с клиническим направлением для UI
        adjusted_shap = shap_value
        if direction_key == "increases" and shap_value < 0:
            # Если модель говорит 'снижает', а медицина 'повышает'
            adjusted_shap = max(0.05, abs(shap_value)) 
        elif direction_key == "reduces" and shap_value > 0:
            # Если модель говорит 'повышает', а медицина 'снижает'
            adjusted_shap = min(-0.05, -abs(shap_value))

        direction_loc = LOCALIZATION[lang]["directions"].get(direction_key, direction_key)

        explanations.append({
            "key": feature,
            "factor": feature_loc["name"],
            "direction": direction_loc,
            "raw_direction": direction_key,
            "shap_value": float(adjusted_shap),
            "clinical_note": feature_loc["note"]
        })

    # Метрические предупреждения
    if model_metrics:
        precision = model_metrics.get('precision', 0.5)
        if isinstance(precision, (int, float)) and precision < 0.6:
            for exp in explanations:
                if exp['raw_direction'] == 'increases':
                    exp['clinical_note'] += f" {LOCALIZATION[lang]['metric_warnings'].get('low_precision', '')}"
                    break

    return explanations
