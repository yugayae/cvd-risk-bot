/**
 * Модуль валидации данных пациента
 */

/**
 * Валидирует данные пациента перед отправкой
 * @param {Object} payload - Данные пациента
 * @returns {Object} Результат валидации с ошибками и предупреждениями
 */
export function validatePatientData(payload) {
    if (!payload || typeof payload !== 'object') {
        return {
            isValid: false,
            errors: ['invalid_payload'],
            warnings: [],
            hasWarnings: false
        };
    }
    
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

/**
 * Оценивает мягкие предупреждения на основе данных
 * @param {Object} payload - Данные пациента
 * @param {Array} softWarningRules - Правила для мягких предупреждений
 * @returns {Array} Массив предупреждений
 */
export function evaluateSoftWarnings(payload, softWarningRules) {
    if (!payload || typeof payload !== 'object') {
        return [];
    }
    
    return softWarningRules
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

/**
 * Нормализует числовые значения в payload
 * @param {Object} payload - Исходные данные
 * @returns {Object} Нормализованные данные
 */
export function normalizePayload(payload) {
    const normalized = { ...payload };
    
    for (let key in normalized) {
        if (key !== "ui_language") {
            const numValue = Number(normalized[key]);
            if (!isNaN(numValue) && isFinite(numValue)) {
                normalized[key] = numValue;
            }
        }
    }
    
    return normalized;
}


