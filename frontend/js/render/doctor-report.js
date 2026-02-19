/**
 * Модуль рендеринга отчета для врача
 */

import { generateClinicalInterpretation } from '../utils/interpretation.js';
import { createEmptyPrediction } from '../utils/normalization.js';
import { animateDoctorRiskGauge, probabilityToPercent, getRiskCategory } from '../riskGauge.js';

/**
 * Рендерит отчет для врача
 * @param {Object} data - Данные предсказания
 * @param {Array} softWarnings - Мягкие предупреждения
 * @param {Object} validation - Результат валидации
 * @param {string} currentLang - Текущий язык
 * @param {Object} labels - Локализованные тексты
 * @param {Object} warningTexts - Тексты предупреждений
 * @param {Object} interpretationTemplates - Шаблоны интерпретаций
 */
export function renderDoctorReport(
    data, 
    softWarnings = [], 
    validation = null,
    currentLang,
    labels,
    warningTexts,
    interpretationTemplates
) {
    // Всегда показываем doctor report, даже если данных нет
    if (!data || typeof data !== "object") {
        data = createEmptyPrediction();
    }

    const doctorCard = document.querySelector(".doctor-report");
    if (!doctorCard) return;
    
    // Показываем doctor report
    doctorCard.style.display = "block";

    /* ---------- Model output ---------- */
    const modelOutputSection = doctorCard.querySelector('[data-section="model"]');
    if (modelOutputSection) {
        const ul = modelOutputSection.querySelector("ul");
        if (ul) {
            const riskPercent =
                data?.risk_card?.risk_probability_percent ??
                (data.risk_probability !== undefined && data.risk_probability !== null
                    ? Math.round(data.risk_probability * 100)
                    : "—");

            const riskCategory = data.risk_label ?? data.risk_category ?? "—";
            
            const confidenceText =
                data.confidence_title ??
                data.confidence_level ??
                data.risk_card?.confidence_level ??
                "—";

            // Анимируем gauge для врача если есть данные о риске
            if (riskPercent !== "—" && data.risk_probability !== undefined) {
                const riskCat = getRiskCategory(data.risk_probability);
                animateDoctorRiskGauge(riskPercent, riskCat);
            }

            ul.innerHTML = `
                <li>${labels.predicted_risk || 'Predicted cardiovascular disease risk'}: ${riskPercent !== "—" ? riskPercent + "%" : "—"}</li>
                <li>${labels.risk_category || 'Risk category'}: ${riskCategory}</li>
                <li>${labels.confidence || 'Prediction confidence'}: ${confidenceText}</li>
            `;
        }
    }

    /* ---------- Key contributing factors ---------- */
    const factorsSection = doctorCard.querySelector('[data-section="factors"]');
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
    const clinicalConditionsSection = doctorCard.querySelector('[data-section="conditions"]');
    if (clinicalConditionsSection) {
        const ul = clinicalConditionsSection.querySelector("ul");
        if (ul) {
            ul.innerHTML = "";

            if (
                Array.isArray(data.clinical_conditions) &&
                data.clinical_conditions.length > 0
            ) {
                data.clinical_conditions.forEach(cond => {
                    if (cond && cond.condition) {
                        ul.innerHTML += `
                            <li>
                                <strong>${cond.condition}</strong>
                                ${cond.severity ? `(${cond.severity})` : ""}
                                ${
                                    cond.note
                                        ? `<div class="condition-note">${cond.note}</div>`
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
                ul.innerHTML = `<li>${noConditionsText}</li>`;
            }
        }
    }

    /* ---------- Clinical interpretation ---------- */
    const interpretationSection = doctorCard.querySelector('[data-section="interpretation"]');
    if (interpretationSection) {
        const p = interpretationSection.querySelector("p");
        if (p) {
            try {
                const interpretation = generateClinicalInterpretation(
                    data, 
                    currentLang, 
                    interpretationTemplates
                );
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
    const warningsSection = doctorCard.querySelector('[data-section="warnings"]');
    if (warningsSection) {
        const ul = warningsSection.querySelector("ul");
        if (!ul) return;

        ul.innerHTML = "";

        const hard = Array.isArray(data?.safety_warnings)
            ? data.safety_warnings
            : [];

        // Добавляем hard warnings
        hard.forEach(key => {
            const text =
                warningTexts[currentLang]?.[key] ??
                warningTexts.en?.[key] ??
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

        // Для врача всегда показываем предупреждение, даже если данных нет или они валидны
        // Это важно для клинической практики - врач должен быть предупрежден о возможных ограничениях
        if (ul.innerHTML.trim() === "") {
            // Если нет других предупреждений, показываем стандартное предупреждение о том,
            // что результаты должны интерпретироваться в контексте клинической картины
            const standardWarning = currentLang === 'ru'
                ? 'Результаты модели должны интерпретироваться в контексте полной клинической картины пациента. Модель является вспомогательным инструментом и не заменяет клиническое суждение.'
                : currentLang === 'kr'
                ? '모델 결과는 환자의 전체 임상 상황의 맥락에서 해석되어야 합니다. 모델은 보조 도구이며 임상적 판단을 대체하지 않습니다.'
                : 'Model results should be interpreted in the context of the patient\'s complete clinical picture. The model is an辅助工具 and does not replace clinical judgment.';
            ul.innerHTML = `<li style="color: #3b82f6; font-weight: 500;">ℹ️ ${standardWarning}</li>`;
        } else {
            // Если есть другие предупреждения, добавляем стандартное предупреждение в конец
            const standardWarning = currentLang === 'ru'
                ? 'Результаты модели должны интерпретироваться в контексте полной клинической картины пациента.'
                : currentLang === 'kr'
                ? '모델 결과는 환자의 전체 임상 상황의 맥락에서 해석되어야 합니다.'
                : 'Model results should be interpreted in the context of the patient\'s complete clinical picture.';
            ul.innerHTML += `<li style="color: #3b82f6; font-weight: 500; margin-top: 8px;">ℹ️ ${standardWarning}</li>`;
        }
    }
}


