// ===============================
// SECTION 1: Constants & Texts
// ===============================
const MODEL_SCOPE_LABELS = {
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

const PATIENT_SAFETY_TEXT = {
    en: {
        title: "Important notice",
        message:
            "Some of the provided values are outside the typical ranges used for model training.",
        advice:
            "The risk estimate is shown, but the result should be interpreted with caution. Consider consulting a healthcare professional."
    },
    ru: {
        title: "Важная информация",
        message:
            "Некоторые из введённых значений выходят за пределы типичных диапазонов, использованных при обучении модели.",
        advice:
            "Оценка риска показана, однако результат следует интерпретировать с осторожностью. Рекомендуется консультация врача."
    },
    kr: {
        title: "중요 안내",
        message:
            "입력된 일부 값이 모델 학습에 사용된 일반적인 범위를 벗어났습니다.",
        advice:
            "위험도 평가는 제공되었으나 결과 해석 시 주의가 필요합니다. 의료 전문가와 상담을 권장합니다."
    }
};

const UI_TEXT = {
    ru: {
        probability: "Вероятность риска",
        factors: "Ключевые клинические факторы"
    },
    en: {
        probability: "Risk probability",
        factors: "Key clinical factors"
    },
    kr: {
        probability: "위험 확률",
        factors: "주요 임상 요인"
    }
};

const DOCTOR_INTERPRETATION_TEMPLATES = {
    en: {
        high_high:
            "The model indicates a high cardiovascular risk driven by clinically significant factors, including {factors}. Given the high confidence of the prediction, clinical intervention and intensive risk factor management should be strongly considered.",
        high_medium:
            "The model indicates a high cardiovascular risk associated with factors such as {factors}. Clinical evaluation and preventive intervention are recommended.",
        moderate:
            "The model suggests a moderate cardiovascular risk associated with factors such as {factors}. Lifestyle modification and regular monitoring are advised.",
        low:
            "The model indicates a low cardiovascular risk. Continued adherence to healthy lifestyle practices is recommended."
    },

    ru: {
        high_high:
            "Модель указывает на высокий сердечно-сосудистый риск, обусловленный клинически значимыми факторами, включая {factors}. Учитывая высокую достоверность прогноза, рекомендуется активное клиническое вмешательство и коррекция факторов риска.",
        high_medium:
            "Модель указывает на высокий сердечно-сосудистый риск, связанный с такими факторами, как {factors}. Рекомендуется клиническая оценка и профилактические меры.",
        moderate:
            "Модель предполагает умеренный сердечно-сосудистый риск, связанный с факторами, такими как {factors}. Рекомендуются изменения образа жизни и регулярное наблюдение.",
        low:
            "Модель указывает на низкий сердечно-сосудистый риск. Рекомендуется поддерживать здоровый образ жизни."
    },

    kr: {
        high_high:
            "모델은 {factors}와 같은 임상적으로 중요한 요인에 의해 높은 심혈관 위험도를 시사합니다. 예측 신뢰도가 높으므로 적극적인 임상적 개입과 위험 요인 관리가 권장됩니다.",
        high_medium:
            "모델은 {factors}와 관련된 높은 심혈관 위험도를 나타냅니다. 임상적 평가 및 예방적 개입이 권장됩니다.",
        moderate:
            "모델은 {factors}와 연관된 중등도의 심혈관 위험도를 시사합니다. 생활 습관 개선과 정기적인 모니터링이 권장됩니다.",
        low:
            "모델은 낮은 심혈관 위험도를 나타냅니다. 건강한 생활 습관을 유지하는 것이 권장됩니다."
    }
};

const WARNING_TEXTS = {
    en: {
        young_age: "The model is less accurate for patients under 40 years old",
        bp_inversion: "Systolic blood pressure is lower than diastolic. Please check the accuracy of the input data.",
        underweight: "Body mass index indicates underweight. Interpretation of cardiovascular risk may differ.",
        very_old_age: "The patient's age exceeds the range used during model training. Prediction reliability may be reduced.",
        extreme_bp: "Blood pressure values are outside the typical clinical ranges observed during model training.",
        extreme_bmi: "Extremely high BMI value detected. Model prediction may be unreliable.",
        low_confidence: "The prediction is close to clinical threshold values. Interpret the result with caution."
    },
    ru: {
        young_age: "Модель менее точна для пациентов моложе 40 лет.",
        bp_inversion: "Систолическое давление ниже диастолического. Проверьте корректность введённых данных.",
        underweight: "Индекс массы тела указывает на недостаточный вес. Интерпретация риска может отличаться.",
        very_old_age: "Возраст пациента превышает диапазон обучения модели. Надёжность прогноза может быть снижена.",
        extreme_bp: "Значения артериального давления выходят за пределы типичных клинических диапазонов.",
        extreme_bmi: "Обнаружено экстремально высокое значение ИМТ. Прогноз модели может быть ненадёжным.",
        low_confidence: "Прогноз близок к клиническому порогу. Интерпретируйте результат с осторожностью."
    },
    kr: {
        young_age: "40세 미만 환자에서는 모델의 정확도가 낮을 수 있습니다.",
        bp_inversion: "수축기 혈압이 이완기 혈압보다 낮습니다. 입력값을 확인하십시오.",
        underweight: "체질량지수가 저체중 범위를 나타냅니다. 위험도 해석이 달라질 수 있습니다.",
        very_old_age: "환자의 연령이 모델 학습 범위를 초과합니다. 예측 신뢰도가 낮을 수 있습니다.",
        extreme_bp: "혈압 수치가 모델 학습 시 관찰된 임상 범위를 벗어났습니다.",
        extreme_bmi: "극단적으로 높은 BMI 값이 감지되었습니다. 모델 예측이 부정확할 수 있습니다.",
        low_confidence: "예측 결과가 임상적 경계값에 근접해 있습니다. 주의해서 해석하십시오."
    }
};

const PATIENT_SUMMARY_TEXTS = {
    en: {
        age: "Age",
        years: "years",
        sex: "Sex",
        male: "Male",
        female: "Female",
        bmi: "Body mass index",
        bp: "Blood pressure",
        smoking: "Smoking status",
        alcohol: "Alcohol consumption",
        activity: "Physical activity",
        yes: "Yes",
        no: "No"
    },
    ru: {
        age: "Возраст",
        years: "лет",
        sex: "Пол",
        male: "Мужской",
        female: "Женский",
        bmi: "Индекс массы тела",
        bp: "Артериальное давление",
        smoking: "Курение",
        alcohol: "Алкоголь",
        activity: "Физическая активность",
        yes: "Да",
        no: "Нет"
    },
    kr: {
        age: "나이",
        years: "세",
        sex: "성별",
        male: "남성",
        female: "여성",
        bmi: "체질량지수",
        bp: "혈압",
        smoking: "흡연",
        alcohol: "음주",
        activity: "신체 활동",
        yes: "예",
        no: "아니오"
    }
};

const DOCTOR_TITLES = {
    en: {
        doctor_view: "Clinical Risk Assessment (Doctor View)",
        patient_summary: "Patient data summary",
        model_output_clinical: "Model output (clinical)",
        factors: "Key contributing factors",
        clinical_conditions: "Clinical conditions",
        interpretation: "Clinical interpretation",
        warnings: "Warnings & model limitations",
        disclaimer: "Disclaimer",
        disclaimer_text:
            "This tool is intended for clinical decision support only and does not replace professional medical advice."
    },
    ru: {
        doctor_view: "Клиническая оценка сердечно-сосудистого риска (врач)",
        patient_summary: "Клинические данные пациента",
        model_output_clinical: "Результаты модели (клинические)",
        factors: "Ключевые клинические факторы",
        clinical_conditions: "Клинические состояния",
        interpretation: "Клиническая интерпретация",
        warnings: "Предупреждения и ограничения модели",
        disclaimer: "Отказ от ответственности",
        disclaimer_text:
            "Данный инструмент предназначен только для поддержки клинических решений и не заменяет профессиональную медицинскую консультацию."
    },
    kr: {
        doctor_view: "임상 심혈관 위험 평가 (의사용)",
        patient_summary: "환자 임상 정보 요약",
        model_output_clinical: "모델 결과 (임상)",
        factors: "주요 임상 요인",
        clinical_conditions: "임상 상태",
        interpretation: "임상적 해석",
        warnings: "경고 및 모델 한계",
        disclaimer: "면책 조항",
        disclaimer_text:
            "이 도구는 임상적 의사결정을 지원하기 위한 것이며 전문적인 의료 조언을 대체하지 않습니다."
    }
};

const DOCTOR_LABELS = {
    en: {
        predicted_risk: "Predicted cardiovascular disease risk",
        risk_category: "Risk category",
        confidence: "Prediction confidence",
        confidence_explanation: "Confidence level indicates how far the predicted risk probability is from clinical decision thresholds (10% and 20%). Higher confidence means the prediction is more stable and reliable.",
        confidence_high: "High confidence: Prediction is ≥7% away from risk thresholds, indicating stable and reliable results.",
        confidence_moderate: "Moderate confidence: Prediction is 3-7% away from risk thresholds, requiring clinical interpretation.",
        confidence_low: "Low confidence: Prediction is <3% away from risk thresholds, indicating uncertainty and requiring cautious interpretation.",
        no_warnings: "No clinical warnings provided",
        model_output_clinical: "Model output (clinical)",
        clinical_conditions_note: "Note: Clinical conditions listed here are supporting context based on input parameters, not medical diagnoses. They represent potential risk factors that may contribute to cardiovascular risk assessment.",
    },    
    ru: {
        predicted_risk: "Прогнозируемый сердечно-сосудистый риск",
        risk_category: "Категория риска",
        confidence: "Достоверность прогноза",
        confidence_explanation: "Уровень достоверности показывает, насколько прогнозируемая вероятность риска удалена от клинических пороговых значений (10% и 20%). Более высокая достоверность означает более стабильный и надежный прогноз.",
        confidence_high: "Высокая достоверность: Прогноз удален ≥7% от пороговых значений риска, что указывает на стабильные и надежные результаты.",
        confidence_moderate: "Умеренная достоверность: Прогноз находится на расстоянии 3-7% от пороговых значений риска, требует клинической интерпретации.",
        confidence_low: "Низкая достоверность: Прогноз находится <3% от пороговых значений риска, что указывает на неопределенность и требует осторожной интерпретации.",
        no_warnings: "Клинические предупреждения отсутствуют",
        model_output_clinical: "Результаты модели (клинические)",
        clinical_conditions_note: "Примечание: Клинические состояния, перечисленные здесь, являются поддерживающим контекстом на основе введенных параметров, а не медицинскими диагнозами. Они представляют потенциальные факторы риска, которые могут способствовать оценке сердечно-сосудистого риска.",
    },
    kr: {
        predicted_risk: "예측된 심혈관 질환 위험",
        risk_category: "위험 범주",
        confidence: "예측 신뢰도",
        confidence_explanation: "신뢰도 수준은 예측된 위험 확률이 임상적 결정 임계값(10% 및 20%)에서 얼마나 떨어져 있는지를 나타냅니다. 높은 신뢰도는 예측이 더 안정적이고 신뢰할 수 있음을 의미합니다.",
        confidence_high: "높은 신뢰도: 예측이 위험 임계값에서 ≥7% 떨어져 있어 안정적이고 신뢰할 수 있는 결과를 나타냅니다.",
        confidence_moderate: "중간 신뢰도: 예측이 위험 임계값에서 3-7% 떨어져 있어 임상적 해석이 필요합니다.",
        confidence_low: "낮은 신뢰도: 예측이 위험 임계값에서 <3% 떨어져 있어 불확실성을 나타내며 주의 깊은 해석이 필요합니다.",
        no_warnings: "임상적 경고가 제공되지 않았습니다",
        model_output_clinical: "모델 결과 (임상)",
        clinical_conditions_note: "참고: 여기에 나열된 임상 상태는 입력 매개변수를 기반으로 한 지원 컨텍스트이며 의학적 진단이 아닙니다. 이는 심혈관 위험 평가에 기여할 수 있는 잠재적 위험 요인을 나타냅니다.",
    }
};

const PATIENT_LABELS = {
    en: {
        title: "Your cardiovascular risk",
        your_risk: "Your estimated cardiovascular risk is",
        meaning: "This result reflects a cardiovascular risk assessment based on the provided information.",
        description:
            "This result is based on the information you provided and does not replace a medical consultation.",
        unavailable:
            "Risk assessment is unavailable based on the provided information."
    },
    ru: {
        title: "Ваш сердечно-сосудистый риск",
        your_risk: "Ваш ориентировочный сердечно-сосудистый риск составляет",
        meaning: "Этот результат отражает оценку сердечно-сосудистого риска на основе предоставленных данных.",
        description:
            "Результат основан на введённых данных и не заменяет консультацию врача.",
        unavailable:
            "Оценка риска недоступна на основе предоставленных данных."
    },
    kr: {
        title: "심혈관 질환 위험도",
        your_risk: "예상되는 심혈관 질환 위험도는",
        meaning: "이 결과는 제공된 정보를 기반으로 한 심혈관 질환 위험 평가를 반영합니다.",
        description:
            "본 결과는 입력된 정보를 기반으로 하며 의사의 진료를 대체하지 않습니다.",
        unavailable:
            "제공된 정보로는 위험도를 평가할 수 없습니다."
    }
};

const SOFT_WARNING_RULES = [
  {
    id: "bmi_high",
    check: (p) => {
      const bmi = p?.bmi;
      return typeof bmi === 'number' && !isNaN(bmi) && isFinite(bmi) && bmi >= 30;
    },
    message: {
      en: "Obesity may influence cardiovascular risk estimation accuracy.",
      ru: "Ожирение может влиять на точность оценки сердечно-сосудистого риска.",
      kr: "비만은 심혈관 위험 추정 정확도에 영향을 줄 수 있습니다."
    }
  },
  {
    id: "bp_edge",
    check: (p) => {
      const ap_hi = p?.ap_hi;
      const ap_lo = p?.ap_lo;
      return typeof ap_hi === 'number' && typeof ap_lo === 'number' &&
             !isNaN(ap_hi) && !isNaN(ap_lo) && isFinite(ap_hi) && isFinite(ap_lo) &&
             ap_hi > ap_lo && ap_hi < ap_lo + 10;
    },
    message: {
      en: "Blood pressure values are close to physiologically inconsistent ranges.",
      ru: "Значения артериального давления близки к физиологически некорректным.",
      kr: "혈압 값이 생리적으로 일관되지 않은 범위에 가까운 경우가 있습니다."
    }
  },
  {
    id: "age_out_of_scope",
    check: (p) => {
      const age = p?.age_years;
      return typeof age === 'number' && !isNaN(age) && isFinite(age) && age > 90;
    },
    message: {
        en: "Patient age exceeds the upper range of model training. Results may be unreliable.",
        ru: "Возраст пациента превышает верхнюю границу обучения модели. Надёжность прогноза может быть снижена.",
        kr: "환자 연령이 모델 학습 범위를 초과합니다. 결과의 신뢰도가 낮을 수 있습니다."
    }

  }
];

// ===============================
// SECTION 1.5: Risk Gauge Functions
// ===============================
/**
 * Risk color mapping
 */
const RISK_COLORS = {
    low: '#10b981',      // green
    moderate: '#f59e0b',  // yellow
    high: '#ef4444'       // red
};

/**
 * Create and animate risk gauge for patient
 * @param {number} riskPercent - Risk percentage (0-100)
 * @param {string} riskCategory - Risk category ('low', 'moderate', 'high')
 */
function animatePatientRiskGauge(riskPercent, riskCategory) {
    const container = document.getElementById('patient-risk-gauge');
    if (!container) {
        console.warn('Patient risk gauge container not found');
        return;
    }

    const color = RISK_COLORS[riskCategory] || '#6b7280';

    // Create gauge HTML
    container.innerHTML = `
        <div class="risk-gauge">
            <div class="risk-gauge-circle" style="
                background: conic-gradient(${color} 0% ${riskPercent}%, #e5e7eb ${riskPercent}% 100%);
            ">
                <div class="risk-gauge-text">
                    <div class="risk-percentage">${riskPercent}%</div>
                    <div class="risk-label">Risk</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Create and animate risk gauge for doctor
 * @param {number} riskPercent - Risk percentage (0-100)
 * @param {string} riskCategory - Risk category ('low', 'moderate', 'high')
 */
function animateDoctorRiskGauge(riskPercent, riskCategory) {
    const container = document.getElementById('doctor-risk-gauge');
    if (!container) {
        console.warn('Doctor risk gauge container not found');
        return;
    }

    const color = RISK_COLORS[riskCategory] || '#6b7280';

    // Create gauge HTML
    container.innerHTML = `
        <div class="risk-gauge doctor-gauge">
            <div class="risk-gauge-circle" style="
                background: conic-gradient(${color} 0% ${riskPercent}%, #e5e7eb ${riskPercent}% 100%);
            ">
                <div class="risk-gauge-text">
                    <div class="risk-percentage">${riskPercent}%</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Utility function to get risk percentage from probability
 * @param {number} probability - Risk probability (0-1)
 * @returns {number} Risk percentage (0-100)
 */
function probabilityToPercent(probability) {
    if (typeof probability !== 'number' || isNaN(probability)) {
        return 0;
    }
    return Math.round(probability * 100);
}

/**
 * Utility function to get risk category from probability
 * @param {number} probability - Risk probability (0-1)
 * @returns {string} Risk category
 */
function getRiskCategory(probability) {
    if (probability < 0.1) return 'low';
    if (probability < 0.2) return 'moderate';
    return 'high';
}

// ===============================
// SECTION 2: Global State & UI State Handlers
// ===============================
const form = document.getElementById("risk-form");
const resultDiv = document.getElementById("result");
const heightInput = document.getElementById("height_cm");
const weightInput = document.getElementById("weight_kg");
const bmiInput = document.getElementById("bmi");
const languageSelect = document.getElementById("ui_language");
let currentLang = "en";
let isSubmitting = false; // Флаг для предотвращения множественных запросов
languageSelect.addEventListener("change", () => {
    currentLang = languageSelect.value;
    updateDoctorTitles(currentLang);
    updateModelScope(currentLang);
    updateModelScopeTexts(currentLang);
});

function calculateBMI() {
    const height = Number(heightInput.value);
    const weight = Number(weightInput.value);

    if (height > 0 && weight > 0) {
        const bmi = weight / Math.pow(height / 100, 2);
        bmiInput.value = bmi.toFixed(1);
    }
}

heightInput.addEventListener("input", calculateBMI);
weightInput.addEventListener("input", calculateBMI);

// ===============================
// SECTION 3: Non-blocking Validation & Warnings
// ===============================
function validatePatientData(payload) {
    const errors = [];
    const warnings = [];
    
    // Проверка возраста
    const age = payload?.age_years;
    if (typeof age !== 'number' || isNaN(age) || !isFinite(age)) {
        errors.push('age_invalid');
    } else if (age < 18) {
        warnings.push('age_too_young');
    } else if (age > 90) {
        warnings.push('age_too_old');
    }
    
    // Проверка АД
    const ap_hi = payload?.ap_hi;
    const ap_lo = payload?.ap_lo;
    if (typeof ap_hi !== 'number' || isNaN(ap_hi) || !isFinite(ap_hi)) {
        errors.push('sbp_invalid');
    } else if (ap_hi < 90 || ap_hi > 220) {
        warnings.push('sbp_out_of_range');
    }
    
    if (typeof ap_lo !== 'number' || isNaN(ap_lo) || !isFinite(ap_lo)) {
        errors.push('dbp_invalid');
    } else if (ap_lo < 50 || ap_lo > 140) {
        warnings.push('dbp_out_of_range');
    }
    
    if (ap_hi && ap_lo && ap_hi < ap_lo) {
        warnings.push('bp_inversion');
    }
    
    // Проверка BMI
    const bmi = payload?.bmi;
    if (typeof bmi !== 'number' || isNaN(bmi) || !isFinite(bmi)) {
        errors.push('bmi_invalid');
    } else if (bmi < 15 || bmi > 60) {
        warnings.push('bmi_out_of_range');
    }
    
    // Проверка обязательных полей
    const requiredFields = ['cholesterol', 'gluc', 'gender', 'smoke', 'alco', 'active'];
    requiredFields.forEach(field => {
        if (payload[field] === undefined || payload[field] === null || payload[field] === '') {
            errors.push(`${field}_missing`);
        }
    });
    
    return {
        isValid: errors.length === 0,
        errors,
        warnings,
        hasWarnings: warnings.length > 0
    };
}

function evaluateModelValidity(data) {
    return {
        hasPrediction: data?.risk_probability !== null && data?.risk_probability !== undefined,
        warnings: data?.safety_warnings || []
    };
}

function evaluateSoftWarnings(payload) {
  if (!payload || typeof payload !== 'object') {
    return [];
  }
  
  return SOFT_WARNING_RULES
    .filter(rule => {
      try {
        return rule.check(payload);
      } catch (error) {
        console.warn('Soft warning check failed:', rule.id, error);
        return false;
      }
    })
    .map(rule => rule.message);
}

function generateClinicalInterpretation(data, lang) {
    if (!data || typeof data !== 'object') {
        return "Clinical interpretation unavailable";
    }
    
    const risk = data.risk_category;
    const confidence = data.confidence_level;

    const factors = (Array.isArray(data.clinical_explanation) ? data.clinical_explanation : [])
        .slice(0, 3)
        .filter(item => item && item.factor)
        .map(item => item.factor)
        .join(", ") || "general risk factors";

    let key = "low";

    if (risk === "high" && confidence === "high") {
        key = "high_high";
    } else if (risk === "high") {
        key = "high_medium";
    } else if (risk === "moderate") {
        key = "moderate";
    }

    const templates =
        DOCTOR_INTERPRETATION_TEMPLATES[lang] ||
        DOCTOR_INTERPRETATION_TEMPLATES.en;

    const template = templates[key] || templates.low;

    return template.replace("{factors}", factors);
}

// ===============================
// SECTION 4: Report Construction (Patient & Doctor)
// ===============================
function renderPatientResult(data, lang, validation = null) {
    const card = document.querySelector(".patient-report");
    if (!card) return;

    card.style.display = "block";

    const labels = PATIENT_LABELS?.[lang] || PATIENT_LABELS?.en;

    const riskPercent =
        data?.risk_card?.risk_probability_percent ??
        (data.risk_probability !== undefined && data.risk_probability !== null
            ? Math.round(data.risk_probability * 100)
            : null);

    // Всегда показываем результат, даже если данных нет
    if (riskPercent === null || riskPercent === undefined) {
        // Показываем сообщение о недоступности, но все равно показываем карточку
        card.innerHTML = `
            <h2>${labels.title}</h2>
            <p class="patient-warning" style="color: #dc2626; font-weight: 600;">
                ${labels.unavailable}
            </p>
            <div id="patient-risk-gauge"></div>
            ${validation && !validation.isValid 
                ? `<p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
                    ${lang === 'ru' 
                        ? 'Проверьте введенные данные и убедитесь, что все поля заполнены корректно.' 
                        : lang === 'kr'
                        ? '입력한 데이터를 확인하고 모든 필드가 올바르게 채워져 있는지 확인하세요.'
                        : 'Please check your input data and ensure all fields are filled correctly.'}
                   </p>`
                : ''}
        `;
        // Показываем gauge с 0% для невалидных данных
        animatePatientRiskGauge(0, 'low');
        return;
    }

    // Убрали предупреждение отсюда, чтобы избежать дублирования с renderPatientSafetyCard
    const riskCategory = getRiskCategory(data.risk_probability);
    animatePatientRiskGauge(riskPercent, riskCategory);
    
    card.innerHTML = `
        <h2>${labels.title}</h2>

        <p class="patient-risk-value">
            ${labels.your_risk}
            <strong>${riskPercent}%</strong>
        </p>

        <div id="patient-risk-gauge"></div>

        <p class="patient-risk-meaning">
            ${labels.meaning}
        </p>

        <p class="patient-risk-note">
            ${labels.description}
        </p>
    `;
}

function renderDoctorReport(data, softWarnings = [], validation = null) {
    // Всегда показываем doctor report, даже если данных нет
    if (!data || typeof data !== "object") {
        data = createEmptyPrediction();
    }

    const doctorCard = document.querySelector(".doctor-report");
    if (!doctorCard) return;
    
    // Показываем doctor report
    doctorCard.style.display = "block";

    const labels = DOCTOR_LABELS[currentLang] || DOCTOR_LABELS.en;

    const modelOutputSection =
        doctorCard.querySelector('[data-section="model"]');
    const factorsSection =
        doctorCard.querySelector('[data-section="factors"]');
    const clinicalConditionsSection =
        doctorCard.querySelector('[data-section="conditions"]');
    const interpretationSection =
        doctorCard.querySelector('[data-section="interpretation"]');
    const warningsSection =
        doctorCard.querySelector('[data-section="warnings"]');

    /* ---------- Model output ---------- */
    if (modelOutputSection) {
        const ul = modelOutputSection.querySelector("ul");
        if (ul) {
        const riskPercent =
            data?.risk_card?.risk_probability_percent ??
            (data.risk_probability !== undefined && data.risk_probability !== null
                ? Math.round(data.risk_probability * 100)
                : "—");

        const riskCategory = data.risk_label ?? data.risk_category ?? "—";
        
        // Анимируем gauge для врача всегда, даже при невалидных данных
        const displayPercent = riskPercent !== "—" ? riskPercent : 0;
        const displayCategory = (riskPercent !== "—" && data.risk_probability !== undefined) 
            ? getRiskCategory(data.risk_probability) 
            : 'low';
        animateDoctorRiskGauge(displayPercent, displayCategory);
        
        const confidenceLevel = data.confidence_level ?? data.risk_card?.confidence_level ?? null;
        const confidenceTitle = data.confidence_title ?? 
            (confidenceLevel === "high" ? labels.confidence_high :
             confidenceLevel === "moderate" ? labels.confidence_moderate :
             confidenceLevel === "low" ? labels.confidence_low : "—");
        const confidenceNote = data.confidence_note ?? "";
        
        // Форматируем confidence с объяснением
        let confidenceHtml = `${labels.confidence}: <strong>${confidenceTitle || confidenceLevel || "—"}</strong>`;
        if (confidenceNote) {
            confidenceHtml += `<br><span style="font-size: 0.85rem; color: #666; font-style: italic;">${confidenceNote}</span>`;
        }
        if (confidenceLevel && labels.confidence_explanation) {
            confidenceHtml += `<br><span style="font-size: 0.8rem; color: #666; margin-top: 4px; display: block;">${labels.confidence_explanation}</span>`;
        }
        
        ul.innerHTML = `
            <li>${labels.predicted_risk}: ${riskPercent !== "—" ? riskPercent + "%" : "—"}</li>
            <li>${labels.risk_category}: ${riskCategory}</li>
            <li>${confidenceHtml}</li>
        `;
        }
    }

    /* ---------- Key contributing factors ---------- */
    if (factorsSection) {
        const ul = factorsSection.querySelector("ul");
        if (!ul) {
            console.warn("Factors section missing <ul>");
        } else {
            ul.innerHTML = "";

            if (
                Array.isArray(data.clinical_explanation) &&
                data.clinical_explanation.length > 0
            ) {
                let hasItems = false;

                data.clinical_explanation.forEach(item => {
                    if (!item || !item.factor) return;

                    hasItems = true;
                    ul.innerHTML += `
                        <li>
                            <strong>${item.factor}</strong>
                            ${item.clinical_note ? `: ${item.clinical_note}` : ""}
                        </li>
                    `;
                });

                if (!hasItems) {
                    const noFactorsText = currentLang === 'ru'
                        ? 'Клинически значимые факторы не выявлены'
                        : currentLang === 'kr'
                        ? '임상적으로 중요한 요인이 확인되지 않았습니다'
                        : 'No clinically relevant factors identified';
                    ul.innerHTML = `<li>${noFactorsText}</li>`;
                }
            } else {
                const unavailableText = currentLang === 'ru'
                    ? 'Анализ клинических факторов недоступен'
                    : currentLang === 'kr'
                    ? '임상 요인 분석을 사용할 수 없습니다'
                    : 'Clinical factor analysis unavailable';
                ul.innerHTML = `<li>${unavailableText}</li>`;
            }
        }
    }

    /* ---------- Clinical conditions ---------- */
    if (clinicalConditionsSection) {
        const ul = clinicalConditionsSection.querySelector("ul");
        if (ul) {
            ul.innerHTML = "";

            // Добавляем примечание о том, что это supporting context, не диагноз
            const noteText = labels.clinical_conditions_note || "";
            if (noteText) {
                ul.innerHTML += `<li style="font-size: 0.85rem; color: #666; font-style: italic; margin-bottom: 12px; padding: 8px; background-color: #f8f9fa; border-left: 3px solid #6B9FA8;">${noteText}</li>`;
            }

            if (
                Array.isArray(data.clinical_conditions) &&
                data.clinical_conditions.length > 0
            ) {
                data.clinical_conditions.forEach(cond => {
                    if (cond && cond.condition) {
                        const severityText = cond.severity 
                            ? (currentLang === 'ru' 
                                ? `(${cond.severity === 'high' ? 'высокая' : cond.severity === 'moderate' ? 'умеренная' : 'низкая'})`
                                : currentLang === 'kr'
                                ? `(${cond.severity === 'high' ? '높음' : cond.severity === 'moderate' ? '중간' : '낮음'})`
                                : `(${cond.severity})`)
                            : "";
                        
                        ul.innerHTML += `
                            <li style="margin-bottom: 12px;">
                                <strong>${cond.condition}</strong>
                                ${severityText ? ` <span style="font-size: 0.85rem; color: #8B4A4A;">${severityText}</span>` : ""}
                                ${
                                    cond.note
                                        ? `<div class="condition-note" style="margin-top: 4px;">${cond.note}</div>`
                                        : ""
                                }
                            </li>
                        `;
                    }
                });
            } else {
                const noConditionsText = currentLang === 'ru'
                    ? 'Клинически значимые состояния не выявлены'
                    : currentLang === 'kr'
                    ? '임상적으로 중요한 상태가 확인되지 않았습니다'
                    : 'No clinically significant conditions identified';
                ul.innerHTML += `<li>${noConditionsText}</li>`;
            }
        }
    }

    /* ---------- Clinical interpretation ---------- */
    if (interpretationSection) {
        const p = interpretationSection.querySelector("p");
        if (p) {
            try {
                const interpretation = generateClinicalInterpretation(data, currentLang);
                p.textContent = interpretation || (currentLang === 'ru'
                    ? 'Клиническая интерпретация недоступна'
                    : currentLang === 'kr'
                    ? '임상적 해석을 사용할 수 없습니다'
                    : 'Clinical interpretation unavailable');
            } catch (error) {
                console.error("Error generating clinical interpretation:", error);
                p.textContent = currentLang === 'ru'
                    ? 'Клиническая интерпретация недоступна'
                    : currentLang === 'kr'
                    ? '임상적 해석을 사용할 수 없습니다'
                    : 'Clinical interpretation unavailable';
            }
        }
    }

    /* ---------- Warnings ---------- */
    if (warningsSection) {
        const ul = warningsSection.querySelector("ul");
        if (!ul) return;

        ul.innerHTML = "";

        const hard = Array.isArray(data?.safety_warnings)
            ? data.safety_warnings
            : [];

        // Связываем confidence с warnings - если confidence низкий, добавляем специальное предупреждение
        const confidenceLevel = data.confidence_level ?? data.risk_card?.confidence_level;
        if (confidenceLevel === "low") {
            const lowConfidenceWarning = currentLang === 'ru'
                ? '⚠️ Низкая достоверность прогноза: результат близок к пороговым значениям. Требуется дополнительная клиническая оценка.'
                : currentLang === 'kr'
                ? '⚠️ 낮은 예측 신뢰도: 결과가 임계값에 가깝습니다. 추가 임상 평가가 필요합니다.'
                : '⚠️ Low prediction confidence: Result is close to threshold values. Additional clinical assessment required.';
            ul.innerHTML += `<li style="color: #B8860B; font-weight: 600; margin-bottom: 8px;">${lowConfidenceWarning}</li>`;
        } else if (confidenceLevel === "moderate") {
            const moderateConfidenceWarning = currentLang === 'ru'
                ? 'ℹ️ Умеренная достоверность прогноза: результат требует клинической интерпретации в контексте других факторов.'
                : currentLang === 'kr'
                ? 'ℹ️ 중간 예측 신뢰도: 결과는 다른 요인과의 맥락에서 임상적 해석이 필요합니다.'
                : 'ℹ️ Moderate prediction confidence: Result requires clinical interpretation in context of other factors.';
            ul.innerHTML += `<li style="color: #6B9FA8; font-weight: 500; margin-bottom: 8px;">${moderateConfidenceWarning}</li>`;
        }

        // Добавляем hard warnings
        hard.forEach(key => {
            const text =
                WARNING_TEXTS[currentLang]?.[key] ??
                WARNING_TEXTS.en?.[key] ??
                key;
            ul.innerHTML += `<li>${text}</li>`;
        });

        // Добавляем soft warnings
        if (Array.isArray(softWarnings)) {
            softWarnings.forEach(msg => {
                const text = msg?.[currentLang] ?? msg?.en;
                if (text) ul.innerHTML += `<li>${text}</li>`;
            });
        }

        // Добавляем предупреждения о валидации
        if (validation) {
            if (!validation.isValid) {
                const validationText = currentLang === 'ru'
                    ? 'Некоторые введенные данные не соответствуют требованиям модели. Результат может быть неточным.'
                    : currentLang === 'kr'
                    ? '입력된 일부 데이터가 모델 요구사항을 충족하지 않습니다. 결과가 부정확할 수 있습니다.'
                    : 'Some input data does not meet model requirements. Results may be inaccurate.';
                ul.innerHTML += `<li style="color: #dc2626; font-weight: 600;">⚠️ ${validationText}</li>`;
            }
            
            if (validation.hasWarnings) {
                const warningsText = currentLang === 'ru'
                    ? 'Введенные данные выходят за рекомендуемые диапазоны модели. Интерпретируйте результат с осторожностью.'
                    : currentLang === 'kr'
                    ? '입력된 데이터가 모델의 권장 범위를 벗어났습니다. 결과를 주의해서 해석하십시오.'
                    : 'Input data is outside model recommended ranges. Interpret results with caution.';
                ul.innerHTML += `<li style="color: #f59e0b; font-weight: 600;">⚠️ ${warningsText}</li>`;
            }
        }

        // Если нет предупреждений, показываем стандартное сообщение
        if (ul.innerHTML.trim() === "") {
            const noWarningsText = DOCTOR_LABELS[currentLang]?.no_warnings 
                ?? DOCTOR_LABELS.en?.no_warnings 
                ?? "No clinical warnings provided";
            ul.innerHTML = `<li>${noWarningsText}</li>`;
        }
    }
}

// ===============================
// SECTION 5: DOM Manipulation
// ===============================
const printBtn = document.getElementById("printDoctorReport");

if (printBtn) {
    printBtn.addEventListener("click", () => {
        window.print();
    });
}

const exportJsonBtn = document.getElementById("exportDoctorJSON");

if (exportJsonBtn) {
    exportJsonBtn.addEventListener("click", () => {
        if (!window.lastPredictionData) return;

        const data = {
            model_output: {
                risk_probability: window.lastPredictionData.risk_probability,
                risk_category: window.lastPredictionData.risk_category,
                confidence_level: window.lastPredictionData.confidence_level
            },
            clinical_explanation: window.lastPredictionData.clinical_explanation,
            clinical_conditions: window.lastPredictionData.clinical_conditions,
            safety_warnings: window.lastPredictionData.safety_warnings,
            audit: window.lastPredictionData.audit
        };

        const blob = new Blob(
            [JSON.stringify(data, null, 2)],
            { type: "application/json" }
        );

        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "clinical_cvd_report.json";
        a.click();
        URL.revokeObjectURL(url);
    });
}

function renderPatientSafetyCard(lang, validation = null) {
    const resultRoot = document.getElementById("result");
    if (!resultRoot) return;

    // удалить старую safety-карточку если была (но не error-warning)
    const old = resultRoot.querySelector(".risk-warning:not(.error-warning)");
    if (old) old.remove();

    const t = PATIENT_SAFETY_TEXT[lang] || PATIENT_SAFETY_TEXT.en;

    let warningMessage = t.message;
    let adviceMessage = t.advice;
    
    // Добавляем информацию о валидации если есть
    if (validation && (!validation.isValid || validation.hasWarnings)) {
        if (!validation.isValid) {
            warningMessage += ` ${currentLang === 'ru' 
                ? 'Некоторые обязательные поля не заполнены или содержат неверные значения.' 
                : currentLang === 'kr'
                ? '일부 필수 필드가 채워지지 않았거나 잘못된 값을 포함하고 있습니다.'
                : 'Some required fields are missing or contain invalid values.'}`;
        }
    }

    const div = document.createElement("div");
    div.className = "card risk-card risk-warning";
    div.innerHTML = `
        <h2>⚠️ ${t.title}</h2>
        <p>${warningMessage}</p>
        <p>${adviceMessage}</p>
    `;
    resultRoot.prepend(div);
}

function showModelLimitations(lang) {
    // Показываем информацию об ограничениях модели с визуальным выделением
    const modelScopeInfo = document.querySelector(".model-scope-info");
    if (modelScopeInfo) {
        modelScopeInfo.style.display = "block";
        modelScopeInfo.style.border = "2px solid #f59e0b";
        modelScopeInfo.style.borderRadius = "8px";
        modelScopeInfo.style.padding = "12px";
        modelScopeInfo.style.backgroundColor = "#fffbeb";
        modelScopeInfo.style.marginTop = "16px";
        modelScopeInfo.style.marginBottom = "16px";
        
        // Добавляем предупреждающий заголовок если его нет
        let warningHeader = modelScopeInfo.querySelector(".model-limitations-warning");
        if (!warningHeader) {
            warningHeader = document.createElement("div");
            warningHeader.className = "model-limitations-warning";
            warningHeader.style.color = "#f59e0b";
            warningHeader.style.fontWeight = "600";
            warningHeader.style.marginBottom = "8px";
            warningHeader.textContent = lang === 'ru'
                ? '⚠️ Ограничения модели:'
                : lang === 'kr'
                ? '⚠️ 모델 제한사항:'
                : '⚠️ Model Limitations:';
            modelScopeInfo.insertBefore(warningHeader, modelScopeInfo.firstChild);
        }
    }
}

function hideModelLimitations() {
    // Скрываем визуальное выделение ограничений модели
    const modelScopeInfo = document.querySelector(".model-scope-info");
    if (modelScopeInfo) {
        modelScopeInfo.style.border = "";
        modelScopeInfo.style.backgroundColor = "";
        modelScopeInfo.style.padding = "";
        const warningHeader = modelScopeInfo.querySelector(".model-limitations-warning");
        if (warningHeader) {
            warningHeader.remove();
        }
    }
}

function updateDoctorTitles(lang) {
    const titles = DOCTOR_TITLES[lang] || DOCTOR_TITLES.en;

    const doctorCard = document.querySelector(".doctor-report");
    if (!doctorCard) return;

    const h2 = doctorCard.querySelector("h2");
    if (h2 && titles.doctor_view) {
        h2.textContent = titles.doctor_view;
    }
    
    const sections = doctorCard.querySelectorAll(".doctor-section");

    sections.forEach(section => {
        const h3 = section.querySelector("h3");
        if (!h3) return;

        const type = section.dataset.section;

        if (type === "patient" && titles.patient_summary)
            h3.textContent = titles.patient_summary;
        else if (type === "model" && titles.model_output_clinical)
            h3.textContent = titles.model_output_clinical;
        else if (type === "factors" && titles.factors)
            h3.textContent = titles.factors;
        else if (type === "conditions" && titles.clinical_conditions)
            h3.textContent = titles.clinical_conditions;
        else if (type === "interpretation" && titles.interpretation)
            h3.textContent = titles.interpretation;
        else if (type === "warnings" && titles.warnings)
            h3.textContent = titles.warnings;
        else if (type === "disclaimer" && titles.disclaimer)
            h3.textContent = titles.disclaimer;
    });
    const disclaimerSection =
        doctorCard.querySelector('[data-section="disclaimer"]');

    if (disclaimerSection) {
        const p = disclaimerSection.querySelector("p");
        if (p && titles.disclaimer_text) {
            p.textContent = titles.disclaimer_text;
        }
    }    
}

function renderPatientSummary(payload, lang) {
    if (!payload || typeof payload !== 'object') {
        console.warn('Invalid payload for renderPatientSummary');
        return;
    }
    
    const section = document.querySelector(
        ".doctor-section.patient-summary"
    );
    if (!section) return;

    const ul = section.querySelector("ul");
    if (!ul) {
        console.warn('Patient summary <ul> not found');
        return;
    }
    
    ul.innerHTML = "";

    const t = PATIENT_SUMMARY_TEXTS[lang] || PATIENT_SUMMARY_TEXTS.en;

    const ageValue = (typeof payload.age_years === 'number' && isFinite(payload.age_years))
        ? `${payload.age_years} ${t.years}`
        : "—";
    
    const bmiValue = (typeof payload.bmi === "number" && isFinite(payload.bmi))
        ? `${payload.bmi.toFixed(1)} kg/m²`
        : "—";
    
    const bpValue = (typeof payload.ap_hi === 'number' && typeof payload.ap_lo === 'number' &&
                     isFinite(payload.ap_hi) && isFinite(payload.ap_lo))
        ? `${payload.ap_hi} / ${payload.ap_lo} mmHg`
        : "—";

    // Улучшенные описания параметров
    const getCholesterolText = (value) => {
        if (value === 1 || value === '1') return lang === 'ru' ? 'Нормальный' : lang === 'kr' ? '정상' : 'Normal';
        if (value === 2 || value === '2') return lang === 'ru' ? 'Выше нормы' : lang === 'kr' ? '정상 이상' : 'Above normal';
        if (value === 3 || value === '3') return lang === 'ru' ? 'Высокий' : lang === 'kr' ? '높음' : 'High';
        return "—";
    };

    const getGlucoseText = (value) => {
        if (value === 1 || value === '1') return lang === 'ru' ? 'Нормальный' : lang === 'kr' ? '정상' : 'Normal';
        if (value === 2 || value === '2') return lang === 'ru' ? 'Выше нормы' : lang === 'kr' ? '정상 이상' : 'Above normal';
        if (value === 3 || value === '3') return lang === 'ru' ? 'Высокий' : lang === 'kr' ? '높음' : 'High';
        return "—";
    };

    const getSmokingText = (value) => {
        const isSmoking = (value === 1 || value === '1');
        if (isSmoking) {
            return lang === 'ru' 
                ? 'Да (курение является независимым фактором сердечно-сосудистого риска)'
                : lang === 'kr'
                ? '예 (흡연은 심혈관 위험의 독립적인 요인입니다)'
                : 'Yes (smoking is an independent cardiovascular risk factor)';
        }
        return t.no;
    };

    const getAlcoholText = (value) => {
        const isDrinking = (value === 1 || value === '1');
        if (isDrinking) {
            return lang === 'ru'
                ? 'Да (регулярное употребление алкоголя связано с повышенным риском)'
                : lang === 'kr'
                ? '예 (정기적인 음주는 위험 증가와 관련이 있습니다)'
                : 'Yes (regular alcohol consumption is associated with increased risk)';
        }
        return t.no;
    };

    const getActivityText = (value) => {
        const isActive = (value === 1 || value === '1');
        if (!isActive) {
            return lang === 'ru'
                ? 'Нет (низкая физическая активность повышает сердечно-сосудистый риск)'
                : lang === 'kr'
                ? '아니오 (낮은 신체 활동은 심혈관 위험을 증가시킵니다)'
                : 'No (low physical activity increases cardiovascular risk)';
        }
        return lang === 'ru'
            ? 'Да (регулярная физическая активность снижает риск)'
            : lang === 'kr'
            ? '예 (정기적인 신체 활동은 위험을 감소시킵니다)'
            : 'Yes (regular physical activity reduces risk)';
    };

    const items = [
        { label: t.age, value: ageValue },
        { 
            label: t.sex, 
            value: (payload.gender === 2 || payload.gender === '2') ? t.male : t.female 
        },
        { label: t.bmi, value: bmiValue },
        { label: t.bp, value: bpValue },
        {
            label: lang === 'ru' ? 'Холестерин' : lang === 'kr' ? '콜레스테롤' : 'Cholesterol',
            value: getCholesterolText(payload.cholesterol)
        },
        {
            label: lang === 'ru' ? 'Глюкоза' : lang === 'kr' ? '혈당' : 'Glucose',
            value: getGlucoseText(payload.gluc)
        },
        {
            label: t.smoking,
            value: getSmokingText(payload.smoke)
        },
        {
            label: t.alcohol,
            value: getAlcoholText(payload.alco)
        },
        {
            label: t.activity,
            value: getActivityText(payload.active)
        }
    ];

    items.forEach(item => {
        if (item.value !== undefined && item.value !== null && item.value !== "") {
            ul.innerHTML += `
                <li style="margin-bottom: 10px;">
                    <strong>${item.label}:</strong> ${item.value}
                </li>
            `;
        }
    });
}

function resetPatientState() {
    // Удаляем только error-warning, но не все предупреждения (они могут быть полезны)
    document.querySelectorAll(".error-warning").forEach(el => el.remove());

    // Сбрасываем patient report (скрываем, но не удаляем)
    const patient = document.querySelector(".patient-report");
    if (patient) {
        patient.style.display = "none";
    }

    // Очищаем patient risk gauge
    const patientGauge = document.getElementById('patient-risk-gauge');
    if (patientGauge) {
        patientGauge.innerHTML = '';
    }

    // НЕ скрываем doctor report - он должен быть всегда виден
    // Просто очищаем данные, но оставляем структуру
    const doctor = document.querySelector(".doctor-report");
    if (doctor) {
        doctor.style.display = "block"; // Убеждаемся что виден
        
        doctor.querySelectorAll("[data-section] ul").forEach(ul => {
            ul.innerHTML = "<li>—</li>";
        });

        doctor.querySelectorAll("[data-section] p").forEach(p => {
            if (!p.closest("[data-section='disclaimer']")) {
                p.textContent = "—";
            }
        });
    }

    // Очищаем doctor risk gauge
    const doctorGauge = document.getElementById('doctor-risk-gauge');
    if (doctorGauge) {
        doctorGauge.innerHTML = '';
    }
    
    // НЕ очищаем глобальные переменные здесь - они могут понадобиться при ошибках
    // Очистка будет происходить только при новом успешном запросе
}

// ===============================
// SECTION 6: Submit Flow (Predict Request)
// ===============================
form.addEventListener("submit", async function (event) {
    event.preventDefault();
    
    // Предотвращаем множественные одновременные запросы
    if (isSubmitting) {
        console.warn('Form submission already in progress');
        return;
    }
    
    isSubmitting = true;
    
    // Блокируем форму во время запроса
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton?.textContent || "Assess Risk";
    
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
    }
    
    try {
        resetPatientState();
        
        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());
        payload.ui_language = currentLang;

        // Приводим числа с валидацией
        for (let key in payload) {
            if (key !== "ui_language") {
                const numValue = Number(payload[key]);
                // Проверяем, что это валидное число
                if (!isNaN(numValue) && isFinite(numValue)) {
                    payload[key] = numValue;
                } else {
                    // Если не число, оставляем как есть (для строковых значений)
                    console.warn(`Invalid number for ${key}: ${payload[key]}`);
                }
            }
        }

        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || `HTTP error! status: ${response.status}`);
        }

        let raw;
        try {
            raw = await response.json();
        } catch (jsonError) {
            console.error("JSON parse error:", jsonError);
            throw new Error("Invalid response format from server");
        }
        
        const data = normalizePrediction(raw);
        const validation = validatePatientData(payload);
        const softWarnings = evaluateSoftWarnings(payload);

        // Объединяем все предупреждения, убирая дубликаты
        const safetyWarnings = Array.isArray(data.safety_warnings) ? data.safety_warnings : [];
        const softWarningsArray = Array.isArray(softWarnings) ? softWarnings : [];
        
        // Убираем дубликаты: если предупреждение уже есть в safety_warnings, не добавляем его из softWarnings
        const uniqueSoftWarnings = softWarningsArray.filter(sw => {
            // Проверяем, нет ли похожего предупреждения в safety_warnings
            const swText = sw?.[currentLang] || sw?.en || '';
            return !safetyWarnings.some(hw => {
                const hwText = warningTexts?.[currentLang]?.[hw] || warningTexts?.en?.[hw] || hw;
                return hwText.toLowerCase().includes(swText.toLowerCase().substring(0, 20)) ||
                       swText.toLowerCase().includes(hwText.toLowerCase().substring(0, 20));
            });
        });
        
        const allWarnings = [...safetyWarnings, ...uniqueSoftWarnings];

        // Добавляем предупреждения о невалидности данных
        if (data.data_validation && !data.data_validation.is_valid) {
            const validationWarning = currentLang === 'ru' 
                ? 'Введенные данные не соответствуют рекомендуемым диапазонам. Результат рассчитан, но интерпретируйте с осторожностью.'
                : currentLang === 'kr'
                ? '입력된 데이터가 권장 범위에 맞지 않습니다. 결과가 계산되었지만 신중하게 해석하세요.'
                : 'Input data does not meet recommended ranges. Result calculated, but interpret with caution.';
            allWarnings.push(validationWarning);
        }

        // Сохраняем данные для экспорта и восстановления при ошибках
        window.lastPredictionData = data;
        window.lastPayload = payload;
        window.lastValidation = validation;

        /* 1. Заголовки и локализация */
        updateDoctorTitles(currentLang);

        /* 2. Patient summary - всегда показываем */
        renderPatientSummary(payload, currentLang);

        /* 3. Doctor report - всегда показываем, даже при ошибках */
        const doctorLabels = {
            predicted_risk: currentLang === 'ru' ? 'Предсказанный риск сердечно-сосудистых заболеваний' : currentLang === 'kr' ? '예측된 심혈관 질환 위험' : 'Predicted cardiovascular disease risk',
            risk_category: currentLang === 'ru' ? 'Категория риска' : currentLang === 'kr' ? '위험 범주' : 'Risk category',
            confidence: currentLang === 'ru' ? 'Достоверность прогноза' : currentLang === 'kr' ? '예측 신뢰도' : 'Prediction confidence'
        };
        renderDoctorReport(data, softWarnings, validation, currentLang, doctorLabels);

        /* 4. Patient result - всегда показываем */
        const patientLabels = {
            title: currentLang === 'ru' ? 'Ваш результат' : currentLang === 'kr' ? '귀하의 결과' : 'Your Result',
            your_risk: currentLang === 'ru' ? 'Ваш риск сердечно-сосудистых заболеваний:' : currentLang === 'kr' ? '귀하의 심혈관 질환 위험:' : 'Your cardiovascular disease risk:',
            meaning: currentLang === 'ru' ? 'Это означает...' : currentLang === 'kr' ? '이는 다음을 의미합니다...' : 'This means...',
            description: currentLang === 'ru' ? 'Обратитесь к врачу для подробной консультации.' : currentLang === 'kr' ? '자세한 상담을 위해 의사와 상의하세요.' : 'Please consult with your doctor for detailed advice.',
            unavailable: currentLang === 'ru' ? 'Результат недоступен' : currentLang === 'kr' ? '결과를 사용할 수 없습니다' : 'Result unavailable'
        };
        renderPatientResult(data, currentLang, validation, patientLabels);

        /* 5. Предупреждения - показываем если есть */
        if (allWarnings.length > 0 || validation.hasWarnings || !validation.isValid) {
            renderPatientSafetyCard(currentLang, validation);
        }
        
        /* 6. Показываем ограничения модели если данные невалидны */
        if (!validation.isValid || validation.hasWarnings) {
            showModelLimitations(currentLang);
        } else {
            // Скрываем выделение если данные валидны
            hideModelLimitations();
        }

    } catch (error) {
        console.error("Submit error:", error);

        // Пытаемся показать что можем, даже при ошибке
        const validation = validatePatientData(window.lastPayload || {});
        
        // Показываем patient summary если есть данные
        if (window.lastPayload) {
            try {
                renderPatientSummary(window.lastPayload, currentLang);
            } catch (e) {
                console.error("Error rendering patient summary:", e);
            }
        }

        // Показываем doctor report с пустыми данными
        try {
            renderDoctorReport(
                window.lastPredictionData || createEmptyPrediction(),
                [],
                validation
            );
        } catch (e) {
            console.error("Error rendering doctor report:", e);
        }

        // Показываем patient result с ошибкой
        try {
            renderPatientResult(
                window.lastPredictionData || createEmptyPrediction(),
                currentLang,
                validation
            );
        } catch (e) {
            console.error("Error rendering patient result:", e);
        }

        // Показываем предупреждение об ошибке
        const t = PATIENT_SAFETY_TEXT[currentLang] || PATIENT_SAFETY_TEXT.en;
        
        if (resultDiv) {
            // Не очищаем полностью, добавляем предупреждение
            const existingWarning = resultDiv.querySelector(".error-warning");
            if (existingWarning) {
                existingWarning.remove();
            }
            
            const errorDiv = document.createElement("div");
            errorDiv.className = "card risk-card risk-warning error-warning";
            errorDiv.innerHTML = `
                <h2>⚠️ ${t.title}</h2>
                <p><strong>Error:</strong> ${error.message || t.message}</p>
                <p>${t.advice}</p>
                <p style="font-size: 0.85rem; color: #666; margin-top: 10px;">
                    ${currentLang === 'ru' 
                        ? 'Проверьте введенные данные и попробуйте снова.' 
                        : currentLang === 'kr'
                        ? '입력한 데이터를 확인하고 다시 시도하세요.'
                        : 'Please check your input and try again.'}
                </p>
            `;
            resultDiv.prepend(errorDiv);
        }

        // Показываем ограничения модели
        showModelLimitations(currentLang);
    } finally {
        // Разблокируем форму в любом случае
        isSubmitting = false;
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    }
});

function normalizePrediction(data) {
    if (!data || typeof data !== 'object') {
        return createEmptyPrediction();
    }
    
    return {
        // Основные поля риска
        risk_category:
            data.risk_category ??
            data.risk_card?.risk_category ??
            null,

        risk_label:
            data.risk_label ??
            data.risk_card?.risk_label ??
            null,

        risk_probability:
            data.risk_probability ??
            data.risk_card?.risk_probability ??
            null,

        risk_probability_percent:
            data.risk_card?.risk_probability_percent ??
            (typeof data.risk_probability === "number" && isFinite(data.risk_probability)
                ? Math.round(data.risk_probability * 100)
                : null),

        // Confidence
        confidence_level:
            data.confidence_level ??
            data.risk_card?.confidence_level ??
            null,

        confidence_title:
            data.confidence_title ??
            data.risk_card?.confidence_title ??
            null,

        confidence_note:
            data.confidence_note ??
            data.risk_card?.confidence_note ??
            null,

        // Клинические данные
        clinical_explanation:
            Array.isArray(data.clinical_explanation)
                ? data.clinical_explanation
                : [],

        clinical_conditions:
            Array.isArray(data.clinical_conditions)
                ? data.clinical_conditions
                : [],

        safety_warnings:
            Array.isArray(data.safety_warnings)
                ? data.safety_warnings
                : [],

        // Дополнительные поля
        risk_card: data.risk_card || null,
        disclaimer: data.disclaimer || null,
        audit: data.audit || null
    };
}

function createEmptyPrediction() {
    return {
        risk_category: null,
        risk_label: null,
        risk_probability: null,
        risk_probability_percent: null,
        confidence_level: null,
        confidence_title: null,
        confidence_note: null,
        clinical_explanation: [],
        clinical_conditions: [],
        safety_warnings: [],
        risk_card: null,
        disclaimer: null,
        audit: null
    };
}
// ===============================
// SECTION 7: Utility Functions
// ===============================
function updateModelScope(lang) {
    const l = MODEL_SCOPE_LABELS[lang] || MODEL_SCOPE_LABELS.en;

    const title = document.querySelector('[data-i18n="model_scope_title"]');
    const desc = document.querySelector('[data-i18n="model_scope_description"]');

    if (!title || !desc) return;

    title.textContent = l.title;
    desc.textContent = l.description;
}

function updateModelScopeTexts(lang) {
  const dict = MODEL_SCOPE_LABELS[lang];
  if (!dict) return;

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
}

async function loadModelMetrics() {
    try {
        const response = await fetch("http://127.0.0.1:8000/metrics");
        if (response.ok) {
            const metrics = await response.json();
            // Сохраняем метрики для использования в renderDoctorReport
            window.modelMetrics = metrics;
        } else {
            console.warn("Failed to load model metrics");
        }
    } catch (error) {
        console.error("Error loading model metrics:", error);
    }
}

function updateDisplayedMetrics(metrics) {
    // Function removed as performance section is no longer displayed
}

document.addEventListener("DOMContentLoaded", () => {
    updateDoctorTitles(currentLang);
    updateModelScope(currentLang);
    updateModelScopeTexts(currentLang);
    loadModelMetrics();
});