/**
 * Утилиты для нормализации данных ответа API
 */

/**
 * Создает пустой объект предсказания
 * @returns {Object} Пустой объект предсказания
 */
export function createEmptyPrediction() {
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

/**
 * Нормализует ответ от API в единый формат
 * @param {Object} data - Сырые данные от API
 * @returns {Object} Нормализованные данные
 */
export function normalizePrediction(data) {
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


