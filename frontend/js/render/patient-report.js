/**
 * Модуль рендеринга отчета для пациента
 */

import { animatePatientRiskGauge, probabilityToPercent, getRiskCategory } from '../riskGauge.js';

/**
 * Рендерит результат для пациента
 * @param {Object} data - Данные предсказания
 * @param {string} lang - Язык
 * @param {Object} validation - Результат валидации
 * @param {Object} labels - Локализованные тексты
 */
export function renderPatientResult(data, lang, validation = null, labels) {
    const card = document.querySelector(".patient-report");
    if (!card) return;

    card.style.display = "block";

    const riskPercent =
        data?.risk_card?.risk_probability_percent ??
        (data.risk_probability !== undefined && data.risk_probability !== null
            ? Math.round(data.risk_probability * 100)
            : null);

    // Всегда показываем результат, даже если данных нет
    if (riskPercent === null || riskPercent === undefined) {
        card.innerHTML = `
            <h2>${labels.title}</h2>
            <p class="patient-warning" style="color: #dc2626; font-weight: 600;">
                ${labels.unavailable}
            </p>
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
        return;
    }

    // Показываем результат с предупреждением если есть проблемы с валидацией
    const warningNote = ((validation && !validation.isValid) || (data.data_validation && !data.data_validation.is_valid))
        ? `<p style="font-size: 0.85rem; color: #f59e0b; margin-top: 8px; font-weight: 600;">
            ⚠️ ${lang === 'ru' 
                ? 'Результат показан, но некоторые данные выходят за рекомендуемые диапазоны.' 
                : lang === 'kr'
                ? '결과가 표시되었지만 일부 데이터가 권장 범위를 벗어났습니다.'
                : 'Result shown, but some data is outside recommended ranges.'}
          </p>`
        : '';

    // Определяем цвет на основе категории риска
    const riskColors = {
        low: '#10b981',      // green
        moderate: '#f59e0b',  // yellow
        high: '#ef4444'       // red
    };
    const riskColor = riskColors[data.risk_category] || '#6b7280'; // default gray

    // Используем модульную функцию для анимации gauge
    const riskCategory = getRiskCategory(data.risk_probability);
    animatePatientRiskGauge(riskPercent, riskCategory);

    card.innerHTML = `
        <h2>${labels.title}</h2>

        <p class="patient-risk-value">
            ${labels.your_risk}
            <strong>${riskPercent}%</strong>
        </p>

        <p class="patient-risk-meaning">
            ${labels.meaning}
        </p>

        <p class="patient-risk-note">
            ${labels.description}
        </p>
        
        ${warningNote}
    `;
}


