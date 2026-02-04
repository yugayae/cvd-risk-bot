// ===============================
// SECTION 1: Constants & Texts
// ===============================

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

// Export other constants similarly...
// (This is a template - you would move all constants here)

