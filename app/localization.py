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
            "moderate": {
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
            "age": {
                "name": "Возраст",
                "note": "Возраст пациента является значимым фактором сердечно-сосудистого риска."
            },
            "height": {
                "name": "Рост",
                "note": "Рост пациента используется для расчета индекса массы тела."
            },
            "weight": {
                "name": "Вес",
                "note": "Повышенный вес может способствовать увеличению нагрузки на сердце."
            },
            "ap_hi": {
                "name": "Систолическое АД",
                "note": "Систолическое артериальное давление ≥ 140 мм рт. ст. указывает на гипертензию."
            },
            "ap_lo": {
                "name": "Диастолическое АД",
                "note": "Диастолическое артериальное давление ≥ 90 мм рт. ст. повышает сердечно-сосудистый риск."
            },
            "cholesterol": {
                "name": "Уровень холестерина",
                "note": "Уровень общего холестерина является ключевым фактором развития атеросклероза."
            },
            "bmi": {
                "name": "Индекс массы тела",
                "note": "ИМТ ≥ 30 кг/м² указывает на ожирение, что повышает риск сердечно-сосудистых осложнений."
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
            "gender": {
                "name": "Пол",
                "note": "Пол пациента влияет на базовый уровень сердечно-сосудистого риска."
            }
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
        ),
        "bot": {
            "welcome": "👋 **Добро пожаловать в CardioRisk AI!**\n\nЯ помогу вам оценить риск сердечно-сосудистых заболеваний.\n\n⚠️ **Отказ от ответственности:** Результаты носят информационный характер и не являются медицинской консультацией. Все результаты должны интерпретироваться врачом.\n\n📊 Доступно сегодня: {count} из {limit}",
            "select_lang": "Пожалуйста, выберете язык / Please select your language / 언어를 선택하세요:",
            "select_region": "Выберите ваш регион (стандарт ВОЗ):",
            "region_unknown": "Неизвестно",
            "consent_request": "Мы не записываем ваш ID или личные данные — все полностью обезличено. Эти данные помогают нам улучшить модель. Вы согласны на сохранение?",
            "consent_yes": "✅ Да, согласен",
            "consent_no": "❌ Нет, спасибо",
            "consent_thanks": "Спасибо за участие! Это никак не влияет на точность вашего результата.",
            "main_menu": "Выберите действие:",
            "btn_new_assessment": "📈 Анализ ({count}/{limit})",
            "btn_help": "❓ Помощь",
            "btn_about": "ℹ️ О системе",
            "btn_tips": "💡 Советы",
            "help_text": "Доступные команды:\n/start - Начальное меню\n/assess - Начать анализ\n/help - Справка",
            "about_text": "CardioRisk AI использует алгоритмы машинного обучения для оценки риска сердечно-сосудистых заболеваний.",
            "tips_text": "Регулярно проверяйте давление, следите за весом и уровнем холестерина.",
            "cooldown": "⏳ Пожалуйста, подождите 30 секунд перед следующим запросом.",
            "limit_reached": "⛔️ К сожалению, ваш дневной лимит ({limit}) исчерпан. Попробуйте завтра!",
            "dob_prompt": "Введите вашу дату рождения (ДД.ММ.ГГГГ, например: 15.05.1985):",
            "dob_error": "❌ Неверный формат даты. Пожалуйста, используйте ДД.ММ.ГГГГ",
            "chol_hint": "💡 **Подсказка:**\n• *Норма:* анализы в норме.\n• *Выше нормы:* врач упоминал пограничные значения или рекомендовал диету.\n• *Высокий:* врач сообщал о выраженном повышении или назначал лекарства.",
            "gluc_hint": "💡 **Подсказка:**\n• *Норма:* уровень сахара в норме.\n• *Выше нормы:* врач упоминал 'преддиабет' или диету.\n• *Высокий:* сахар значительно повышен или назначено лечение.",
            "clinical_guidance": "⚠️ Этот вопрос только для ориентировочной оценки и не заменяет лабораторные анализы.",
            "smoke_clarification": "🚬 Курение вейпов, сигар и кальяна также считается курением.",
            "alco_clarification": "🍷 Вопрос носит субъективный характер. Если вы употребляете алкоголь хотя бы изредка — лучше ответить 'Да'."
        }
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
            "moderate": {
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
            "age": {
                "name": "나이",
                "note": "환자의 나이는 심혈관 위험의 중요한 요소입니다."
            },
            "height": {
                "name": "키",
                "note": "신장은 체질량 지수를 계산하는 데 사용됩니다."
            },
            "weight": {
                "name": "몸무게",
                "note": "과체중은 심장 부하를 증가시킬 수 있습니다."
            },
            "ap_hi": {
                "name": "수축기 혈압",
                "note": "수축기 혈압 ≥ 140 mmHg는 고혈압을 나타냅니다."
            },
            "ap_lo": {
                "name": "이완기 혈압",
                "note": "이완기 혈압 ≥ 90 mmHg는 심혈관 위험을 증가시킵니다."
            },
            "cholesterol": {
                "name": "콜레스테롤 수치",
                "note": "총 콜레스테롤 수치 상승은 죽상동맹글경화증 발병의 핵심 요소입니다."
            },
            "bmi": {
                "name": "체질량 지수",
                "note": "BMI ≥ 30 kg/m²는 심혈관 합병증 위험을 높이는 비만을 나타냅니다."
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
            },
            "gender": {
                "name": "성별",
                "note": "환자의 성별은 기본적인 심혈관 위험 수준에 영향을 미칩니다."
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
        ),
        "bot": {
            "welcome": "👋 **CardioRisk AI에 오신 것을 환영합니다!**\n\nAI를 통해 심혈관 질환 위험을 평가해 드립니다.\n\n⚠️ **면책조항:** 본 결과는 정보 제공용이며 의학적 진단을 대체할 수 없습니다. 모든 결과는 전문의의 해석이 필요합니다.\n\n📊 오늘의 남은 횟수: {limit} 중 {count}",
            "select_lang": "언어를 선택하세요 / Пожалуйста, выберете язык / Please select your language:",
            "select_region": "거주 지역을 선택하세요 (WHO 표준):",
            "region_unknown": "알 수 없음",
            "consent_request": "우리는 귀하의 ID나 개인 정보를 기록하지 않으며, 모든 데이터는 완전히 익명화됩니다. 이 데이터는 우리의 모델을 개선하는 데 도움이 됩니다. 저장을 동의하십니까?",
            "consent_yes": "✅ 네, 동의합니다",
            "consent_no": "❌ 아니요, 괜찮습니다",
            "consent_thanks": "참여해 주셔서 감사합니다! 이는 검사 결과의 정확도에 영향을 주지 않습니다.",
            "main_menu": "작업을 선택하세요:",
            "btn_new_assessment": "📈 분석 ({count}/{limit})",
            "btn_help": "❓ 도움말",
            "btn_about": "ℹ️ 시스템 정보",
            "btn_tips": "💡 건강 팁",
            "help_text": "사용 가능한 명령어:\n/start - 시작 메뉴\n/assess - 분석 시작\n/help - 도움말",
            "about_text": "CardioRisk AI는 머신러닝 알고리즘을 사용하여 심혈관 질환 위험을 평가합니다.",
            "tips_text": "정기적으로 혈압을 체크하고 체중과 콜레스테롤 수치를 관리하세요.",
            "cooldown": "⏳ 다음 요청까지 30초만 기다려 주세요.",
            "limit_reached": "⛔️ 죄송합니다. 오늘의 요청 한도({limit}회)를 모두 사용하셨습니다. 내일 다시 시도해 주세요!",
            "dob_prompt": "생년월일을 입력해 주세요 (DD.MM.YYYY, 예: 15.05.1985):",
            "dob_error": "❌ 날짜 형식이 올바르지 않습니다. DD.MM.YYYY 형식을 사용해 주세요.",
            "chol_hint": "💡 **참고:**\n• *정상:* 수치가 정상 범위 내에 있음.\n• *관리 필요:* 의사가 경계치라고 언급했거나 식단 조절을 권고함.\n• *높음:* 의사가 상당한 수치 상승을 알렸거나 약물 치료를 권고함.",
            "gluc_hint": "💡 **참고:**\n• *정상:* 혈당 수치가 정상임.\n• *관리 필요:* 의사가 '내당능 장애'를 언급했거나 식단 조절을 권고함.\n• *높음:* 혈당이 상당히 높거나 치료를 받고 있음.",
            "clinical_guidance": "⚠️ 이 질문은 오직 참고용이며 실험실 정밀 검사를 대체할 수 없습니다.",
            "smoke_clarification": "🚬 전자담배, 시가, 물담배 등도 흡연 상태에 해당합니다.",
            "alco_clarification": "🍷 이 질문은 주관적입니다. 아주 가끔이라도 술을 마신다면 '예'라고 답하는 것이 좋습니다."
        }
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
            "moderate": {
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
            "age": {
                "name": "Age",
                "note": "Patient age is a significant factor in cardiovascular risk."
            },
            "height": {
                "name": "Height",
                "note": "Patient height is used for BMI calculation."
            },
            "weight": {
                "name": "Weight",
                "note": "Increased weight can contribute to cardiac strain."
            },
            "ap_hi": {
                "name": "Systolic Blood Pressure",
                "note": "Systolic blood pressure ≥ 140 mmHg indicates hypertension."
            },
            "ap_lo": {
                "name": "Diastolic Blood Pressure",
                "note": "Diastolic blood pressure ≥ 90 mmHg increases cardiovascular risk."
            },
            "cholesterol": {
                "name": "Cholesterol Level",
                "note": "Total cholesterol level is a key factor in atherosclerosis development."
            },
            "bmi": {
                "name": "Body Mass Index",
                "note": "BMI ≥ 30 kg/m² indicates obesity, which increases risk."
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
            },
            "gender": {
                "name": "Sex",
                "note": "Patient sex influences the baseline cardiovascular risk level."
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
        ),
        "bot": {
            "welcome": "👋 **Welcome to CardioRisk AI!**\n\nI can help you assess your cardiovascular risk using an advanced AI model.\n\n⚠️ **Disclaimer:** Results are for informational purposes only and do not constitute medical advice. All results must be interpreted by a physician.\n\n📊 Available today: {count} of {limit}",
            "select_lang": "Please select your language / Пожалуйста, выберете язык / 언어를 선택하세요:",
            "select_region": "Select your region (WHO standard):",
            "region_unknown": "Unknown",
            "consent_request": "We do not record your ID or personal information — everything is fully anonymized. This data helps us improve the model. Do you consent to saving?",
            "consent_yes": "✅ Yes, I consent",
            "consent_no": "❌ No, thanks",
            "consent_thanks": "Thank you for participating! This does not affect the accuracy of your assessment.",
            "main_menu": "Select an action:",
            "btn_new_assessment": "📈 Analysis ({count}/{limit})",
            "btn_help": "❓ Help",
            "btn_about": "ℹ️ About System",
            "btn_tips": "💡 Health Tips",
            "help_text": "Available commands:\n/start - Main menu\n/assess - Start assessment\n/help - Help",
            "about_text": "CardioRisk AI uses machine learning algorithms to assess cardiovascular disease risk.",
            "tips_text": "Monitor your blood pressure, weight, and cholesterol levels regularly.",
            "cooldown": "⏳ Please wait 30 seconds before your next request.",
            "limit_reached": "⛔️ Sorry, your daily limit ({limit}) has been reached. Please try again tomorrow!",
            "dob_prompt": "Enter your date of birth (DD.MM.YYYY, e.g., 15.05.1985):",
            "dob_error": "❌ Invalid date format. Please use DD.MM.YYYY",
            "chol_hint": "💡 **Hint:**\n• *Normal:* Previous tests were normal.\n• *Above Normal:* Doctor mentioned borderline values or recommended a diet.\n• *High:* Doctor reported significant elevation or recommended medication.",
            "gluc_hint": "💡 **Hint:**\n• *Normal:* Sugar levels are within range.\n• *Above Normal:* Doctor mentioned 'pre-diabetes' or a diet.\n• *High:* Sugar is significantly elevated or treatment is prescribed.",
            "clinical_guidance": "⚠️ This question is for orientation only and does not replace laboratory tests.",
            "smoke_clarification": "🚬 Smoking vapes, cigars, and hookahs also counts as smoking.",
            "alco_clarification": "🍷 This question is subjective. If you drink even occasionally, it's better to answer 'Yes'."
        }
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


