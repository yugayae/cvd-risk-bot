LOCALIZATION = {
    "ru": {
        "risk_category": {
            "low": "Низкий сердечно-сосудистый риск",
            "moderate": "Умеренный сердечно-сосудистый риск",
            "high": "Высокий сердечно-сосудистый риск"
        },
        "confidence": {
            "high": {
                "title": "Высокая достоверность прогноза",
                "note": "Прогноз стабилен и уверенно отличается от пороговых значений риска."
            },
            "medium": {
                "title": "Умеренная достоверность прогноза",
                "note": "Прогноз близок к пороговым значениям риска и требует клинической интерпретации."
            },
            "low": {
                "title": "Низкая достоверность прогноза",
                "note": "Прогноз нестабилен и должен интерпретироваться с осторожностью."
            }
        },
        "warnings": {
            "young_age": "Модель менее точна у пациентов младше 40 лет",
            "bp_inversion": "Систолическое давление ниже диастолического. Проверьте корректность введённых данных.",
            "underweight": "Индекс массы тела указывает на недостаточный вес. Интерпретация сердечно-сосудистого риска может отличаться.",
            "very_old_age": "Возраст пациента превышает диапазон, использованный при обучении модели. Достоверность прогноза может быть снижена.",
            "extreme_bp": "Значения артериального давления выходят за пределы типичных клинических диапазонов, наблюдавшихся при обучении модели.",
            "extreme_bmi": "Обнаружено экстремально высокое значение ИМТ. Прогноз модели может быть ненадёжным.",
            "low_confidence": "Прогноз близок к клиническому пороговому значению. Интерпретируйте результат с осторожностью."
        },
        "metric_warnings": {
            "low_precision": "Примечание: Модель имеет умеренную точность, рассмотрите дополнительную клиническую оценку.",
            "moderate_discrimination": "Дискриминация модели умеренная, интерпретируйте результаты осторожно."
        },
        "risk_card": {
            "headline": {
                "high": "Высокий сердечно-сосудистый риск",
                "moderate": "Умеренный сердечно-сосудистый риск",
                "low": "Низкий сердечно-сосудистый риск"
            },
            "summary": {
                "high": "Пациент имеет высокий сердечно-сосудистый риск. Основные факторы: {factors}. Рекомендуется клиническое вмешательство.",
                "moderate": "Выявлен умеренный сердечно-сосудистый риск, обусловленный факторами: {factors}. Рекомендовано наблюдение и коррекция образа жизни.",
                "low": "Сердечно-сосудистый риск низкий. Значимые факторы риска не выявлены."
            }
        },
        "shap_factors": {
            "sbp": {
                "name": "Систолическое артериальное давление",
                "note": "Систолическое артериальное давление ≥ 140 мм рт. ст."
            },
                 
            "gluc": {
                "name": "Уровень глюкозы",
                "note": "Повышенный уровень глюкозы крови ассоциирован с повышенным сердечно-сосудистым риском."
            },
            "smoke": {
                "name": "Курение",
                "note": "Курение является независимым фактором сердечно-сосудистого риска."
            },
            "active": {
                "name": "Физическая активность",
                "note": "Низкий уровень физической активности повышает сердечно-сосудистый риск."
            },
            "alco": {
                "name": "Алкоголь",
                "note": "Регулярное употребление алкоголя связано с повышенным сердечно-сосудистым риском."
            },
        },
        "clinical_factors": {
            "cholesterol_attention": {
                "name": "Уровень холестерина",
                "note": "Уровень холестерина выше нормы. Рекомендуется контроль и коррекция образа жизни."
            },
            "cholesterol_high": {
                "name": "Уровень холестерина",
                "note": "Повышенный уровень общего холестерина ассоциирован с высоким сердечно-сосудистым риском."
            }
        },
        "clinical_conditions": {
            "high_bp": {
                "name": "Артериальная гипертензия",
                "severity": "high",
                "note": "Систолическое артериальное давление ≥ 140 мм рт. ст."
            },
            "obesity": {
                "name": "Ожирение",
                "severity": "moderate",
                "note": "Индекс массы тела ≥ 30 кг/м²."
            }
        },
        "directions": {
            "increases": "повышает риск",
            "reduces": "снижает риск",
            "neutral": "не влияет"
        },
        "doctor_interpretation": {
            "high_high": "Модель указывает на высокий сердечно-сосудистый риск, обусловленный клинически значимыми факторами, включая {factors}. Учитывая высокую достоверность прогноза, рекомендуется активное клиническое вмешательство и коррекция факторов риска.",
            "high_medium": "Выявлен высокий сердечно-сосудистый риск, однако достоверность прогноза умеренная. Результат требует клинической интерпретации.",
            "moderate": "У пациента определяется умеренный сердечно-сосудистый риск, преимущественно за счёт модифицируемых факторов. Рекомендованы изменения образа жизни и динамическое наблюдение.",
            "low": "Сердечно-сосудистый риск низкий. Доминирующие клинически значимые факторы риска не выявлены. Рекомендованы стандартные профилактические мероприятия."
        },  
        "disclaimer": (
            "Данный инструмент предназначен только для клинической поддержки "
            "принятия решений и не заменяет профессиональное медицинское заключение."
        )
    },

    "kr": {
        "risk_category": {
            "low": "낮은 심혈관 위험",
            "moderate": "중등도 심혈관 위험",
            "high": "높은 심혈관 위험"
        },
        "confidence": {
            "high": {
                "title": "예측 신뢰도 높음",
                "note": "예측 결과는 안정적이며 위험 기준값과 명확히 구분됩니다."
            },
            "medium": {
                "title": "예측 신뢰도 중간",
                "note": "예측 결과는 위험 기준값에 근접하여 임상적 해석이 필요합니다."
            },
            "low": {
                "title": "예측 신뢰도 낮음",
                "note": "예측 결과가 불안정하여 주의 깊은 해석이 필요합니다."
            }
        },
        "warnings": {
            "young_age": "40세 미만 환자에서는 모델 정확도가 낮을 수 있습니다",
            "bp_inversion": "수축기 혈압이 이완기 혈압보다 낮습니다. 입력 데이터의 정확성을 확인하세요.",
            "underweight": "체중 지수가 저체중을 나타냅니다. 심혈관 위험의 해석이 달라질 수 있습니다.",
            "very_old_age": "환자의 나이가 모델 학습 시 사용된 범위를 초과합니다. 예측의 신뢰성은 감소할 수 있습니다.",
            "extreme_bp": "혈압 값이 모델 학습 시 관찰된 일반적인 임상 범위를 벗어납니다.",
            "extreme_bmi": "BMI 값이 극단적으로 높습니다. 모델 예측은 신뢰성이 낮을 수 있습니다.",
            "low_confidence": "예측 결과가 임상적 기준치에 가깝습니다. 결과 해석 시 주의가 필요합니다."
        },
        "metric_warnings": {
            "low_precision": "참고: 모델의 정밀도가 중간 수준입니다. 추가 임상 평가를 고려하세요.",
            "moderate_discrimination": "모델 판별력이 중간 수준입니다. 결과를 신중하게 해석하세요."
        },
        "risk_card": {
            "headline": {
                "high": "높은 심혈관 위험",
                "moderate": "중등도 심혈관 위험",
                "low": "낮은 심혈관 위험"
            },
            "summary": {
                "high": "환자는 높은 심혈관 위험을 보입니다. 주요 위험 요인은 {factors}입니다. 임상적 개입이 권장됩니다.",
                "moderate": "환자에게 중등도의 심혈관 위험이 확인되었으며, 이는 다음 요인에 의해 영향을 받습니다: {factors}. 경과 관찰 및 생활습관 교정이 권장됩니다.",
                "low": "심혈관 위험은 낮은 수준입니다. 임상적으로 유의한 위험 요인은 확인되지 않았습니다."
            }
        },
        "shap_factors": {
            "sbp": {
                "name": "수축기 혈압",
                "note": "수축기 혈압 ≥ 140 mmHg"
            },
            "cholesterol": {
                "name": "콜레스테롤 수치",
                "note": "총 콜레스테롤 수치 상승"
            },
            "gluc": {
                "name": "혈당 수치",
                "note": "높은 혈당 수치는 심혈관 위험 증가와 관련이 있습니다."
            },
            "smoke": {
                "name": "흡연 상태",
                "note": "흡연은 독립적인 심혈관 위험 요인입니다."
            },
            "active": {
                "name": "신체 활동",
                "note": "낮은 신체 활동 수준은 심혈관 위험을 증가시킵니다."
            },
            "alco": {
                "name": "음주",
                "note": "규칙적인 음주는 심혈관 위험 증가와 관련이 있습니다."
            }
        },
        "clinical_factors": {
            "cholesterol_attention": {
                "name": "콜레스테롤 수치",
                "note": "콜레스테롤 수치가 정상 범위를 초과합니다. 관리 및 생활습관 교정이 권장됩니다."
            },
            "cholesterol_high": {
                "name": "콜레스테롤 수치",
                "note": "높은 총 콜레스테롤 수치는 높은 심혈관 위험과 관련이 있습니다."
            }
        },
        "clinical_conditions": {
            "high_bp": {
                "name": "고혈압",
                "severity": "high",
                "note": "수축기 혈압 ≥ 140 mmHg"
            },
            "obesity": {
                "name": "비만",
                "severity": "moderate",
                "note": "체질량 지수 ≥ 30 kg/m²"
            }
        },
        "directions": {
            "increases": "위험 증가",
            "reduces": "위험 감소",
            "neutral": "영향 없음"
        },
        "doctor_interpretation": {
            "high_high": "모델은 임상적으로 유의한 요인({factors})에 의해 높은 심혈관 위험을 예측합니다. 예측 신뢰도가 높아 적극적인 임상적 개입과 위험 요인 관리가 권장됩니다.",
            "high_medium": "높은 심혈관 위험이 확인되었으나 예측 신뢰도는 중간 수준입니다. 임상적 판단이 필요합니다.",
            "moderate": "환자는 주로 조절 가능한 요인에 의해 중등도의 심혈관 위험을 보입니다. 생활습관 개선 및 추적 관찰이 권장됩니다.",
            "low": "심혈관 위험은 낮은 수준입니다. 주요 고위험 요인은 확인되지 않았으며, 일반적인 예방 관리가 적절합니다."
        },
        "disclaimer": (
            "이 도구는 임상 의사 결정을 지원하기 위한 목적으로만 사용되며 "
            "전문적인 의료 조언을 대체하지 않습니다."
        )   
    },
    "en": {
        "risk_category": {
            "low": "Low cardiovascular risk",
            "moderate": "Moderate cardiovascular risk",
            "high": "High cardiovascular risk"
        },
        "confidence": {
            "high": {
                "title": "High prediction confidence",
                "note": "The prediction is stable and clearly distinguished from risk thresholds."
            },
            "medium": {
                "title": "Moderate prediction confidence",
                "note": "The prediction is close to risk thresholds and requires clinical interpretation."
            },
            "low": {
                "title": "Low prediction confidence",
                "note": "The prediction is unstable and should be interpreted with caution."
            }
        },
        "warnings": {
            "young_age": "The model is less accurate for patients under 40 years old",
            "bp_inversion": "Systolic blood pressure is lower than diastolic. Please check the accuracy of the input data.",
            "underweight": "Body mass index indicates underweight. Interpretation of cardiovascular risk may differ.",
            "very_old_age": "The patient's age exceeds the range used during model training. Prediction reliability may be reduced.",
            "extreme_bp": "Blood pressure values are outside the typical clinical ranges observed during model training.",
            "extreme_bmi": "Extremely high BMI value detected. Model prediction may be unreliable.",
            "low_confidence": "The prediction is close to clinical threshold values. Interpret the result with caution."
        },
        "metric_warnings": {
            "low_precision": "Note: Model has moderate precision, consider additional clinical evaluation.",
            "moderate_discrimination": "Model discrimination is moderate, interpret results cautiously."
        },
        "risk_card": {
            "headline": {
                "high": "High cardiovascular risk",
                "moderate": "Moderate cardiovascular risk",
                "low": "Low cardiovascular risk"
            },
            "summary": {
                "high": "The patient has a high cardiovascular risk. Key factors: {factors}. Clinical intervention is recommended.",
                "moderate": "A moderate cardiovascular risk has been identified, influenced by factors: {factors}. Monitoring and lifestyle modification are advised.",
                "low": "Cardiovascular risk is low. No clinically significant risk factors were identified."
            }
        },
        "shap_factors": {
            "sbp": {
                "name": "Systolic Blood Pressure",
                "note": "Systolic blood pressure ≥ 140 mmHg"
            },
            "cholesterol": {
                "name": "Cholesterol Level",
                "note": "Elevated total cholesterol level"
            },
            "gluc": {
                "name": "Glucose Level",
                "note": "High blood glucose levels are associated with increased cardiovascular risk."
            },
            "smoke": {
                "name": "Smoking Status",
                "note": "Smoking is an independent cardiovascular risk factor."
            },
            "active": {
                "name": "Physical Activity",
                "note": "Low levels of physical activity increase cardiovascular risk."                    
            },
            "alco": {
                "name": "Alcohol Consumption",
                "note": "Regular alcohol consumption is associated with increased cardiovascular risk."
            }
        },
        "clinical_factors": {
            "cholesterol_attention": {
                "name": "Cholesterol Level",
                "direction": "requires attention",
                "note": "Cholesterol level is above normal. Management and lifestyle modification are recommended."
            },
            "cholesterol_high": {
                "name": "Cholesterol Level",
                "direction": "increases risk",
                "note": "Elevated total cholesterol level is associated with high cardiovascular risk."
            }
        },
        "clinical_conditions": {
            "high_bp": {
                "name": "Hypertension",
                "severity": "high",
                "note": "Systolic blood pressure ≥ 140 mmHg"
            },
            "obesity": {
                "name": "Obesity",
                "severity": "moderate",
                "note": "Body mass index ≥ 30 kg/m²"
            }
        },
        "directions": {
            "increases": "increases risk",
            "reduces": "reduces risk",
            "neutral": "no effect"
        },
        "doctor_interpretation": {
            "high_high": "The model indicates a high cardiovascular risk driven by clinically significant factors including {factors}. Given the high confidence of the prediction, active clinical intervention and risk factor modification are recommended.",
            "high_medium": "A high cardiovascular risk has been identified; however, the prediction confidence is moderate. The result requires clinical interpretation.",
            "moderate": "The patient has a moderate cardiovascular risk, primarily due to modifiable factors. Lifestyle changes and dynamic monitoring are recommended.",
            "low": "Cardiovascular risk is low. No dominant clinically significant risk factors were identified. Standard preventive measures are advised."
        },
        "disclaimer": (
            "This tool is intended for clinical decision support only "
            "and does not replace professional medical advice."
        )
    }
}



def t(lang: str, category: str, key: str = None, subkey: str = None):
    data = LOCALIZATION.get(lang, LOCALIZATION["ru"])

    if key is None:
        return data.get(category)

    value = data.get(category, {}).get(key)

    if isinstance(value, dict) and subkey:
        return value.get(subkey)

    return value


