/**
 * Утилиты для работы с предупреждениями
 */

/**
 * Правила для мягких предупреждений
 */
export const SOFT_WARNING_RULES = [
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


