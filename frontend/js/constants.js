/**
 * Все константы, тексты и конфигурация для приложения
 */

// ===============================
// API Configuration
// ===============================
export const API_BASE_URL = "http://127.0.0.1:8000";
export const API_ENDPOINTS = {
    predict: "/api/predict",
    health: "/api/health",
    metrics: "/api/metrics"
};

// ===============================
// Risk Colors
// ===============================
export const RISK_COLORS = {
    low: '#10b981',      // green
    moderate: '#f59e0b',  // yellow
    high: '#ef4444'       // red
};

export const MODEL_SCOPE_LABELS = {
    en: {
        title: "ℹ️ Model applicability",
        description:
            "The model was trained on adult patient data and performs most reliably within the following parameter ranges. Values outside these ranges do not block calculation but may reduce accuracy.",
        model_scope_param: "Parameter",
        model_scope_range: "Recommended range",
        model_scope_age: "Age",
        model_scope_bmi: "Body mass index (BMI)",
        model_scope_sbp: "Systolic blood pressure",
        model_scope_dbp: "Diastolic blood pressure",
        model_scope_cholesterol: "Cholesterol",
        model_scope_glucose: "Glucose"
    },
    ru: {
        title: "ℹ️ Область применимости модели",
        description:
            "Модель обучалась на данных взрослых пациентов и наиболее надёжно работает в следующих диапазонах параметров. Значения вне этих диапазонов не блокируют расчёт, но могут снижать точность прогноза.",
        model_scope_param: "Параметр",
        model_scope_range: "Рекомендуемый диапазон",
        model_scope_age: "Возраст",
        model_scope_bmi: "Индекс массы тела (ИМТ)",
        model_scope_sbp: "Систолическое АД",
        model_scope_dbp: "Диастолическое АД",
        model_scope_cholesterol: "Холестерин",
        model_scope_glucose: "Глюкоза"
    },
    kr: {
        title: "ℹ️ 모델 적용 범위",
        description:
            "이 모델은 성인 환자 데이터를 기반으로 학습되었으며 다음 범위 내에서 가장 신뢰도가 높습니다. 해당 범위를 벗어난 값도 계산은 가능하지만 정확도가 낮아질 수 있습니다.",
        model_scope_param: "항목",
        model_scope_range: "권장 범위",
        model_scope_age: "나이",
        model_scope_bmi: "체질량지수 (BMI)",
        model_scope_sbp: "수축기 혈압",
        model_scope_dbp: "이완기 혈압",
        model_scope_cholesterol: "콜레스테롤",
        model_scope_glucose: "혈당"
    }
};

export const PATIENT_SAFETY_TEXT = {
    en: {
        title: "Important notice",
        message: "Some of the provided values are outside the typical ranges used for model training.",
        advice: "The risk estimate is shown, but the result should be interpreted with caution. Consider consulting a healthcare professional."
    },
    ru: {
        title: "Важная информация",
        message: "Некоторые из введённых значений выходят за пределы типичных диапазонов, использованных при обучении модели.",
        advice: "Оценка риска показана, однако результат следует интерпретировать с осторожностью. Рекомендуется консультация врача."
    },
    kr: {
        title: "중요 안내",
        message: "입력된 일부 값이 모델 학습에 사용된 일반적인 범위를 벗어났습니다.",
        advice: "위험도 평가는 제공되었으나 결과 해석 시 주의가 필요합니다. 의료 전문가와 상담을 권장합니다."
    }
};

export const DOCTOR_INTERPRETATION_TEMPLATES = {
    en: {
        high_high: "The model indicates a high cardiovascular risk driven by clinically significant factors, including {factors}. Given the high confidence of the prediction, clinical intervention and intensive risk factor management should be strongly considered.",
        high_medium: "The model indicates a high cardiovascular risk associated with factors such as {factors}. Clinical evaluation and preventive intervention are recommended.",
        moderate: "The model suggests a moderate cardiovascular risk associated with factors such as {factors}. Lifestyle modification and regular monitoring are advised.",
        low: "The model indicates a low cardiovascular risk. Continued adherence to healthy lifestyle practices is recommended."
    },
    ru: {
        high_high: "Модель указывает на высокий сердечно-сосудистый риск, обусловленный клинически значимыми факторами, включая {factors}. Учитывая высокую достоверность прогноза, рекомендуется активное клиническое вмешательство и коррекция факторов риска.",
        high_medium: "Модель указывает на высокий сердечно-сосудистый риск, связанный с такими факторами, как {factors}. Рекомендуется клиническая оценка и профилактическое вмешательство.",
        moderate: "Модель предполагает умеренный сердечно-сосудистый риск, связанный с факторами, такими как {factors}. Рекомендуется изменение образа жизни и регулярный мониторинг.",
        low: "Модель указывает на низкий сердечно-сосудистый риск. Рекомендуется продолжать придерживаться здорового образа жизни."
    },
    kr: {
        high_high: "모델은 {factors}를 포함한 임상적으로 중요한 요인으로 인한 높은 심혈관 위험을 나타냅니다. 높은 예측 신뢰도를 고려할 때 임상 개입과 강화된 위험 요인 관리를 강력히 권고합니다.",
        high_medium: "모델은 {factors}와 같은 요인과 관련된 높은 심혈관 위험을 나타냅니다. 임상 평가 및 예방적 개입을 권장합니다.",
        moderate: "모델은 {factors}와 같은 요인과 관련된 중간 정도의 심혈관 위험을 제시합니다. 생활방식 개선 및 정기적인 모니터링을 조언합니다.",
        low: "모델은 낮은 심혈관 위험을 나타냅니다. 건강한 생활습관의 지속을 권장합니다."
    }
};

export const DOCTOR_TITLES = {
    en: {
        doctor_view: "Clinical Risk Assessment (Doctor View)",
        patient_summary: "Patient data summary",
        model_output_clinical: "Model output (clinical)",
        factors: "Key contributing factors",
        clinical_conditions: "Clinical conditions",
        interpretation: "Clinical interpretation",
        warnings: "Warnings & model limitations",
        disclaimer: "Disclaimer",
        disclaimer_text: "This tool is intended for clinical decision support only and does not replace professional medical advice."
    },
    ru: {
        doctor_view: "Клиническая оценка риска (для врача)",
        patient_summary: "Краткая информация о пациенте",
        model_output_clinical: "Результаты модели (клинические)",
        factors: "Ключевые влияющие факторы",
        clinical_conditions: "Клинические состояния",
        interpretation: "Клиническая интерпретация",
        warnings: "Предупреждения и ограничения модели",
        disclaimer: "Дисклеймер",
        disclaimer_text: "Этот инструмент предназначен исключительно для поддержки клинических решений и не заменяет профессиональную медицинскую консультацию."
    },
    kr: {
        doctor_view: "임상 위험 평가 (의사용)",
        patient_summary: "환자 정보 요약",
        model_output_clinical: "모델 결과 (임상)",
        factors: "주요 영향 요인",
        clinical_conditions: "임상 상태",
        interpretation: "임상 해석",
        warnings: "경고 및 모델 제한사항",
        disclaimer: "면책사항",
        disclaimer_text: "이 도구는 임상 의사결정 지원 목적으로만 사용되며 전문 의료 상담을 대체하지 않습니다."
    }
};

export const PATIENT_SUMMARY_TEXTS = {
    en: {
        years: "years",
        male: "Male",
        female: "Female",
        yes: "Yes",
        no: "No",
        age: "Age",
        sex: "Sex",
        bmi: "BMI",
        bp: "Blood Pressure",
        smoking: "Smoking",
        alcohol: "Alcohol",
        activity: "Physical Activity"
    },
    ru: {
        years: "лет",
        male: "Мужчина",
        female: "Женщина",
        yes: "Да",
        no: "Нет",
        age: "Возраст",
        sex: "Пол",
        bmi: "ИМТ",
        bp: "Артериальное давление",
        smoking: "Курение",
        alcohol: "Алкоголь",
        activity: "Физическая активность"
    },
    kr: {
        years: "세",
        male: "남성",
        female: "여성",
        yes: "예",
        no: "아니오",
        age: "나이",
        sex: "성별",
        bmi: "BMI",
        bp: "혈압",
        smoking: "흡연",
        alcohol: "음주",
        activity: "신체 활동"
    }
};

export const PATIENT_LABELS = {
    en: {
        title: "Your Result",
        your_risk: "Your cardiovascular disease risk:",
        meaning: "This means...",
        description: "Please consult with your doctor for detailed advice.",
        unavailable: "Result unavailable"
    },
    ru: {
        title: "Ваш результат",
        your_risk: "Ваш риск сердечно-сосудистых заболеваний:",
        meaning: "Это означает...",
        description: "Обратитесь к врачу для подробной консультации.",
        unavailable: "Результат недоступен"
    },
    kr: {
        title: "귀하의 결과",
        your_risk: "귀하의 심혈관 질환 위험:",
        meaning: "이는 다음을 의미합니다...",
        description: "자세한 상담을 위해 의사와 상의하세요.",
        unavailable: "결과를 사용할 수 없습니다"
    }
};

export const DOCTOR_LABELS = {
    en: {
        predicted_risk: "Predicted cardiovascular disease risk",
        risk_category: "Risk category",
        confidence: "Prediction confidence"
    },
    ru: {
        predicted_risk: "Предсказанный риск сердечно-сосудистых заболеваний",
        risk_category: "Категория риска",
        confidence: "Достоверность прогноза"
    },
    kr: {
        predicted_risk: "예측된 심혈관 질환 위험",
        risk_category: "위험 범주",
        confidence: "예측 신뢰도"
    }
};


