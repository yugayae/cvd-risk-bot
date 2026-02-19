/**
 * Утилиты для генерации клинических интерпретаций
 */

/**
 * Генерирует клиническую интерпретацию на основе данных предсказания
 * @param {Object} data - Данные предсказания
 * @param {string} lang - Язык интерпретации
 * @param {Object} templates - Шаблоны интерпретаций
 * @returns {string} Текст интерпретации
 */
export function generateClinicalInterpretation(data, lang, templates) {
    if (!data || typeof data !== 'object') {
        return getUnavailableText(lang);
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

    const langTemplates = templates[lang] || templates.en || templates;
    const template = langTemplates[key] || langTemplates.low || "";

    return template.replace("{factors}", factors);
}

/**
 * Возвращает текст "недоступно" на нужном языке
 * @param {string} lang - Язык
 * @returns {string} Текст
 */
function getUnavailableText(lang) {
    const texts = {
        ru: "Клиническая интерпретация недоступна",
        kr: "임상적 해석을 사용할 수 없습니다",
        en: "Clinical interpretation unavailable"
    };
    return texts[lang] || texts.en;
}


