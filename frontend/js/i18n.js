/**
 * Multilingual localization system
 * Supports: English, Russian, Korean
 */

const TRANSLATIONS = {
    en: {
        // Header
        header_title: "CVD Risk Analytics | AI-Powered",
        logo_text: "CardioRisk AI",
        lang_kr: "한국어",

        // Form - Demographics
        section_demographics: "Demographics",
        label_region: "Region (WHO)",
        region_unknown: "Unknown",
        label_dob: "Date of Birth",
        label_age: "Age (years)",
        label_gender: "Gender",
        option_male: "Male",
        option_female: "Female",

        // Form - Indicators
        section_indicators: "Indicators",
        label_systolic: "Systolic BP (mmHg)",
        label_diastolic: "Diastolic BP (mmHg)",
        label_cholesterol: "Cholesterol",
        option_normal: "Normal",
        option_above_normal: "Above normal",
        option_high: "High",
        label_glucose: "Glucose",
        label_bmi: "BMI (Body Mass Index)",
        label_height: "Height (cm)",
        label_weight: "Weight (kg)",
        results_bmi: "Patient BMI",

        // Form - Lifestyle
        section_lifestyle: "Lifestyle",
        label_smoking: "Smoking",
        label_alcohol: "Alcohol",
        label_physical_activity: "Physical activity",
        option_yes: "Yes",
        option_no: "No",

        // Buttons
        btn_assess: "Assess Risk",
        btn_calculate: "Calculate Risk",
        btn_print: "Print Report",
        btn_export: "Export JSON",
        btn_accept: "Yes, I agree",
        btn_decline: "No, do not save",

        // Modal
        modal_consent_title: "Data Ethics & Analytics",
        modal_consent_message: "Your anonymous data helps us improve the model's accuracy. No personal identifiers are stored. Do you allow us to save the results of this assessment?",

        // Results
        results_title: "Analysis Results",
        results_empty: "Fill in the form on the left and click \"Calculate\" to get a forecast.",
        results_patient_profile: "Patient Profile",
        results_risk_probability: "Risk Probability",
        results_key_factors: "Key Contributing Factors",
        results_recommendations: "Clinical Interpretation (Second Opinion)",
        results_bmi: "Patient BMI",

        // Risk Categories
        risk_low: "Low Risk",
        risk_moderate: "Moderate Risk",
        risk_high: "High Risk",
        risk_cvd: "Probability of CVD",

        // Recommendations
        default_recommendation: "It is recommended to maintain your current healthy lifestyle in accordance with WHO guidelines.",
        factor_recommendations: {
            "smoke": "Quitting smoking is one of the most effective ways to reduce cardiovascular risk.",
            "alco": "It is recommended to limit alcohol consumption.",
            "active": "Regular physical activity reduces cardiovascular risk.",
            "bmi": "Weight reduction to normal BMI values can lower cardiovascular risk.",
            "obesity": "Weight reduction to normal BMI values can lower cardiovascular risk.",
            "ap_hi": "Blood pressure control and medical consultation for therapy are recommended.",
            "ap_lo": "Blood pressure control and medical consultation for therapy are recommended.",
            "high_bp": "Blood pressure control and medical consultation for therapy are recommended.",
            "cholesterol": "A lipid-lowering diet and cholesterol level monitoring are recommended.",
            "cholesterol_high": "A lipid-lowering diet and cholesterol level monitoring are recommended.",
            "cholesterol_attention": "A lipid-lowering diet and cholesterol level monitoring are recommended.",
            "gluc": "Blood glucose control and specialist consultation are recommended."
        },
        rec_low: "Indicators are normal. Continue maintaining a healthy lifestyle, monitor cholesterol levels, and stay active.",
        rec_moderate: "Warning: elevated risk observed. Review your diet, reduce salt intake, and consult with a cardiologist.",
        rec_high: "CRITICAL LEVEL. Urgent visit to a doctor is strongly recommended for detailed examination and treatment.",

        // Confidence Levels
        confidence_high: "High",
        confidence_moderate: "Moderate",
        confidence_low: "Low",

        // Clinical Info
        clinical_explanation: "Clinical Explanation",
        clinical_conditions: "Clinical Conditions",
        clinical_warnings: "Warnings & Limitations",
        clinical_disclaimer: "Medical Decision Support Disclaimer",

        // Error Messages
        error_form_invalid: "Please fill in all required fields correctly",
        error_validation_age: "Invalid age (must be 18-90)",
        error_api_failed: "Error communicating with server. Please try again.",
        error_calculation: "Error during risk calculation",
        error_network: "Network error. Check your connection.",

        // SHAP Factor Labels
        shap_age: "Age",
        shap_systolic: "Systolic BP",
        shap_cholesterol: "Cholesterol",
        shap_glucose: "Glucose",
        shap_bmi: "BMI",
        shap_smoking: "Smoking",
        shap_alcohol: "Alcohol",
        shap_activity: "Physical Activity",

        // Chart Labels
        chart_risk: "Risk Level",
        chart_safe: "Safe",
        chart_factor_influence: "Factor Influence",
        direction_increases: "Increases risk",
        direction_reduces: "Reduces risk",

        // Clinical Hints & Reference Values
        hint_label: "Clinical Hint",
        hint_selection_feedback: "You selected status '{status}'. For your region it corresponds to: {value}.",
        hint_glucose_1: "No symptoms and stable weight.",
        hint_glucose_2: "BMI > 25, low activity, age 45+.",
        hint_glucose_3: "Thirst, frequent urination, diabetes in relatives.",
        hint_cholesterol_1: "Active lifestyle, no smoking.",
        hint_cholesterol_2: "Smoking, fast food, BP > 130/80.",
        hint_cholesterol_3: "Obesity, xanthelasma, chest pain on exertion.",

        ref_glucose_1: "< 5.6 mmol/L",
        ref_glucose_2: "5.6 - 6.9 mmol/L",
        ref_glucose_3: ">= 7.0 mmol/L",
        ref_cholesterol_1: "< 5.2 mmol/L",
        ref_cholesterol_2: "5.2 - 6.2 mmol/L",
        ref_cholesterol_3: "> 6.2 mmol/L",

        clinical_disclaimer_detailed: "This tool is a clinical decision support system (CDSS) and is not intended for diagnosis or prescribing treatment. Results are a probabilistic risk assessment and must be interpreted by a medical professional.",
    },

    ru: {
        // Заголовок
        header_title: "CVD Risk Analytics | AI-Powered",
        logo_text: "CardioRisk AI",
        lang_en: "English",
        lang_ru: "Русский",
        lang_kr: "한국어",

        // Форма - Демография
        section_demographics: "Демография",
        label_region: "Регион (ВОЗ)",
        region_unknown: "Неизвестно",
        label_dob: "Дата рождения",
        label_age: "Возраст (лет)",
        label_gender: "Пол",
        option_male: "Мужской",
        option_female: "Женский",

        // Форма - Показатели
        section_indicators: "Показатели",
        label_systolic: "Систолическое АД (mmHg)",
        label_diastolic: "Диастолическое АД (mmHg)",
        label_cholesterol: "Холестерин",
        option_normal: "Норма",
        option_above_normal: "Выше нормы",
        option_high: "Высокий",
        label_glucose: "Глюкоза",
        label_bmi: "ИМТ",
        label_height: "Рост (см)",
        label_weight: "Вес (кг)",

        // Форма - Образ жизни
        section_lifestyle: "Образ жизни",
        label_smoking: "Курение",
        label_alcohol: "Алкоголь",
        label_physical_activity: "Физическая активность",
        option_yes: "Да",
        option_no: "Нет",

        // Кнопки
        btn_assess: "Оценить риск",
        btn_calculate: "Рассчитать риск",
        btn_print: "Печать отчета",
        btn_export: "Экспорт JSON",
        btn_accept: "Да, я согласен",
        btn_decline: "Нет, не сохранять",

        // Modal
        modal_consent_title: "Этика данных и аналитика",
        modal_consent_message: "Ваши анонимные данные помогут улучшить точность модели. Личные данные не сохраняются. Разрешаете ли вы сохранить результаты этой оценки?",

        // Результаты
        results_title: "Результаты анализа",
        results_empty: "Заполните форму слева и нажмите \"Рассчитать\", чтобы получить прогноз.",
        results_patient_profile: "Профиль пациента",
        results_risk_probability: "Вероятность риска",
        results_key_factors: "Ключевые факторы влияния",
        results_recommendations: "Клиническая интерпретация (Второе мнение)",
        results_bmi: "ИМТ пациента",

        // Категории риска
        risk_low: "Низкий риск",
        risk_moderate: "Умеренный риск",
        risk_high: "Высокий риск",
        risk_cvd: "Вероятность ССЗ заболеваний",

        // Рекомендации
        default_recommendation: "Рекомендуется придерживаться текущего здорового образа жизни в соответствии с рекомендациями ВОЗ.",
        factor_recommendations: {
            "smoke": "Отказ от курения является одним из наиболее эффективных способов снижения сердечно-сосудистого риска.",
            "alco": "Рекомендуется ограничить потребление алкоголя.",
            "active": "Регулярная физическая активность снижает сердечно-сосудистый риск.",
            "bmi": "Снижение массы тела до нормальных значений ИМТ может снизить сердечно-сосудистый риск.",
            "obesity": "Снижение массы тела до нормальных значений ИМТ может снизить сердечно-сосудистый риск.",
            "ap_hi": "Рекомендуется контроль артериального давления и консультация врача по вопросам терапии.",
            "ap_lo": "Рекомендуется контроль артериального давления и консультация врача по вопросам терапии.",
            "high_bp": "Рекомендуется контроль артериального давления и консультация врача по вопросам терапии.",
            "cholesterol": "Рекомендуется соблюдение гиполипидемической диеты и контроль уровня холестерина.",
            "cholesterol_high": "Рекомендуется соблюдение гиполипидемической диеты и контроль уровня холестерина.",
            "cholesterol_attention": "Рекомендуется соблюдение гиполипидемической диеты и контроль уровня холестерина.",
            "gluc": "Рекомендуется контроль уровня глюкозы и консультация специалиста."
        },
        rec_low: "Показатели в норме. Продолжайте вести здоровый образ жизни, следите за уровнем холестерина и поддерживайте активность.",
        rec_moderate: "Внимание: наблюдается повышенный риск. Рекомендуется пересмотреть диету, сократить потребление соли и проконсультироваться с кардиологом.",
        rec_high: "КРИТИЧЕСКИЙ УРОВЕНЬ. Настоятельно рекомендуется немедленно обратиться к врачу для детального обследования и назначения терапии.",

        // Уровни уверенности
        confidence_high: "Высокая",
        confidence_moderate: "Средняя",
        confidence_low: "Низкая",

        // Клиническая информация
        clinical_explanation: "Клиническое объяснение",
        clinical_conditions: "Клинические условия",
        clinical_warnings: "Предупреждения и ограничения",
        clinical_disclaimer: "Отказ от ответственности",

        // Сообщения об ошибках
        error_form_invalid: "Пожалуйста, заполните все требуемые поля корректно",
        error_api_failed: "Ошибка при соединении с сервером. Пожалуйста, попробуйте снова.",
        error_calculation: "Ошибка при расчете риска",
        error_network: "Ошибка сети. Проверьте подключение.",

        // SHAP метки факторов
        shap_age: "Возраст",
        shap_systolic: "Сист. АД",
        shap_cholesterol: "Холестерин",
        shap_glucose: "Глюкоза",
        shap_bmi: "ИМТ",
        shap_smoking: "Курение",
        shap_alcohol: "Алкоголь",
        shap_activity: "Физическая активность",

        // Метки диаграмм
        chart_risk: "Риск",
        chart_safe: "Безопасно",
        chart_factor_influence: "Влияние фактора",
        direction_increases: "Повышает риск",
        direction_reduces: "Снижает риск",

        // Клинические подсказки и референсные значения
        hint_label: "Подсказка",
        hint_selection_feedback: "Вы выбрали статус '{status}'. Для вашего региона это соответствует значениям: {value}.",
        hint_glucose_1: "Отсутствие симптомов и стабильный вес.",
        hint_glucose_2: "ИМТ > 25, малоподвижность, возраст 45+.",
        hint_glucose_3: "Жажда, частое мочеиспускание, диабет у родственников.",
        hint_cholesterol_1: "Активный образ жизни, отсутствие курения.",
        hint_cholesterol_2: "Курение, фастфуд, давление > 130/80.",
        hint_cholesterol_3: "Ожирение, ксантелазмы, боли в груди при нагрузке.",

        ref_glucose_1: "< 5.6 ммоль/л",
        ref_glucose_2: "5.6 - 6.9 ммоль/л",
        ref_glucose_3: ">= 7.0 ммоль/л",
        ref_cholesterol_1: "< 5.2 ммоль/л",
        ref_cholesterol_2: "5.2 - 6.2 ммоль/л",
        ref_cholesterol_3: "> 6.2 ммоль/л",

        clinical_disclaimer_detailed: "Данный инструмент является системой поддержки принятия врачебных решений (CDSS) и не предназначен для постановки диагноза или назначения лечения. Результаты являются вероятностной оценкой риска и должны интерпретироваться медицинским специалистом.",
    },

    kr: {
        // 헤더
        header_title: "CVD Risk Analytics | AI-Powered",
        logo_text: "CardioRisk AI",
        lang_en: "English",
        lang_ru: "Русский",
        lang_kr: "한국어",

        // 양식 - 인구통계
        section_demographics: "인구통계",
        label_region: "거주 지역 (WHO)",
        region_unknown: "알 수 없음",
        label_dob: "생년월일",
        label_age: "나이 (세)",
        label_gender: "성별",
        option_male: "남성",
        option_female: "여성",

        // 양식 - 지표
        section_indicators: "지표",
        label_systolic: "수축기 혈압 (mmHg)",
        label_diastolic: "이완기 혈압 (mmHg)",
        label_cholesterol: "콜레스테롤",
        option_normal: "정상",
        option_above_normal: "정상 이상",
        option_high: "높음",
        label_glucose: "혈당",
        label_bmi: "BMI",
        label_height: "키 (cm)",
        label_weight: "몸무게 (kg)",

        // 양식 - 생활 방식
        section_lifestyle: "생활 방식",
        label_smoking: "흡연",
        label_alcohol: "알코올",
        label_physical_activity: "신체 활동",
        option_yes: "예",
        option_no: "아니오",

        // 버튼
        btn_assess: "위험 평가",
        btn_calculate: "위험 계산",
        btn_print: "보고서 인쇄",
        btn_export: "JSON 내보내기",
        btn_download_pdf: "PDF 다운로드",

        btn_accept: "예, 동의합니다",
        btn_decline: "아니요, 저장하지 않습니다",

        // Modal
        modal_consent_title: "데이터 윤리 및 분석",
        modal_consent_message: "당신의 익명 데이터는 모델의 정확도를 향상하는 데 도움이 됩니다. 개인 식별 정보는 저장되지 않습니다. 이 평가 결과를 저장하도록 허용하시겠습니까?",

        // 결과
        results_title: "분석 결과",
        results_empty: "왼쪽의 양식을 작성하고 \"계산\"을 클릭하여 예측을 받으세요.",
        results_patient_profile: "환자 프로필",
        results_risk_probability: "위험 확률",
        results_key_factors: "주요 영향 요인",
        results_recommendations: "임상적 해석 (제2의 견해)",
        results_bmi: "환자 BMI",

        // 위험 범주
        risk_low: "저위험",
        risk_moderate: "중간 위험",
        risk_high: "고위험",
        risk_cvd: "심혈관질환 확률",

        // 권장사항
        default_recommendation: "WHO 권장 사항에 따라 현재의 건강한 생활 습관을 유지하는 것이 권장됩니다.",
        factor_recommendations: {
            "smoke": "금연은 심혈관 위험을 줄이는 가장 효과적인 방법 중 하나입니다.",
            "alco": "알코올 섭취를 제한하는 것이 권장됩니다.",
            "active": "규칙적인 신체 활동은 심혈관 위험을 낮춥니다.",
            "bmi": "체중을 정상 BMI 범위로 줄이면 심혈관 위험을 낮출 수 있습니다.",
            "obesity": "체중을 정상 BMI 범위로 줄이면 심혈관 위험을 낮출 수 있습니다.",
            "ap_hi": "혈압 조절 및 치료에 대한 의사 상담이 권장됩니다.",
            "ap_lo": "혈압 조절 및 치료에 대한 의사 상담이 권장됩니다.",
            "high_bp": "혈압 조절 및 치료에 대한 의사 상담이 권장됩니다.",
            "cholesterol": "지질저하 식단을 따르고 콜레스테롤 수치를 관리하는 것이 권장됩니다.",
            "cholesterol_high": "지질저하 식단을 따르고 콜레스테롤 수치를 관리하는 것이 권장됩니다.",
            "cholesterol_attention": "지질저하 식단을 따르고 콜레스테롤 수치를 관리하는 것이 권장됩니다.",
            "gluc": "혈당 수치를 관리하고 전문의와 상담하는 것이 권장됩니다."
        },
        rec_low: "지표가 정상입니다. 건강한 생활 습관을 유지하고 콜레스테롤 수치를 모니터링하며 활동을 계속하세요.",
        rec_moderate: "경고: 상승된 위험이 관찰되었습니다. 식단을 검토하고 염분 섭취를 줄이며 심장 전문의와 상담하세요.",
        rec_high: "심각한 수준입니다. 상세한 검사와 치료를 위해 즉시 의사를 방문할 것을 강력히 권장합니다.",

        // 신뢰도 수준
        confidence_high: "높음",
        confidence_moderate: "중간",
        confidence_low: "낮음",

        // 임상 정보
        clinical_explanation: "임상 설명",
        clinical_conditions: "임상 조건",
        clinical_warnings: "경고 및 제한 사항",
        clinical_disclaimer: "의료 결정 지원 면책조항",

        // 오류 메시지
        error_form_invalid: "모든 필수 필드를 올바르게 작성하십시오",
        error_api_failed: "서버와의 통신 오류. 다시 시도하세요.",
        error_calculation: "위험 계산 중 오류 발생",
        error_network: "네트워크 오류. 연결을 확인하세요.",

        // SHAP 요인 레이블
        shap_age: "나이",
        shap_systolic: "수축기 혈압",
        shap_cholesterol: "콜레스테롤",
        shap_glucose: "혈당",
        shap_bmi: "BMI",
        shap_smoking: "흡연",
        shap_alcohol: "알코올",
        shap_activity: "신체 활동",

        // 차트 레이블
        chart_risk: "위험",
        chart_safe: "안전",
        chart_factor_influence: "요인 영향",
        direction_increases: "위험 증가",
        direction_reduces: "위험 감소",

        // 임상 힌트 및 기준치
        hint_label: "힌트",
        hint_selection_feedback: "'{status}' 상태를 선택했습니다. 귀하의 지역에서는 {value}에 해당합니다.",
        hint_glucose_1: "증상이 없고 체중이 안정적입니다.",
        hint_glucose_2: "BMI > 25, 활동량 부족, 45세 이상.",
        hint_glucose_3: "갈증, 빈뇨, 가족력이 있는 당뇨병.",
        hint_cholesterol_1: "활동적인 생활 방식, 비흡연.",
        hint_cholesterol_2: "흡연, 화스트푸드 섭취, 혈압 > 130/80.",
        hint_cholesterol_3: "비만, 황색판종, 운동 시 가슴 통증.",

        ref_glucose_1: "< 100 mg/dL",
        ref_glucose_2: "100 - 125 mg/dL",
        ref_glucose_3: ">= 126 mg/dL",
        ref_cholesterol_1: "< 200 mg/dL",
        ref_cholesterol_2: "200 - 239 mg/dL",
        ref_cholesterol_3: ">= 240 mg/dL",

        clinical_disclaimer_detailed: "본 도구는 임상 의사결정 지원 시스템(CDSS)이며 진단이나 처방을 위한 것이 아닙니다. 결과는 확률적 위험 평가이며 반드시 의료 전문가에 의해 해석되어야 합니다.",
    }
};

/**
 * Localization manager
 */
class I18n {
    constructor(defaultLang = 'en') {
        this.currentLang = defaultLang;
    }

    setLanguage(lang) {
        if (TRANSLATIONS[lang]) {
            this.currentLang = lang;
            document.documentElement.lang = lang;
            return true;
        }
        return false;
    }

    t(key, fallback = null) {
        const translation = TRANSLATIONS[this.currentLang]?.[key];
        if (translation) return translation;

        // Fallback to English
        const fallbackTrans = TRANSLATIONS['en']?.[key];
        if (fallbackTrans) return fallbackTrans;

        // Return custom fallback or key itself
        return fallback || key;
    }

    getLanguage() {
        return this.currentLang;
    }

    // Bulk translate object
    translateObject(obj) {
        const result = {};
        for (const [key, value] of Object.entries(obj)) {
            result[key] = this.t(key, value);
        }
        return result;
    }
}

// Global instance
const i18n = new I18n('en');

export { i18n, TRANSLATIONS };
