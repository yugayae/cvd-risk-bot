/**
 * Утилиты для работы с формой
 */

/**
 * Инициализирует обработчики для расчета BMI
 * @param {HTMLElement} heightInput - Поле ввода роста
 * @param {HTMLElement} weightInput - Поле ввода веса
 * @param {HTMLElement} bmiInput - Поле вывода BMI
 */
export function initializeBMICalculator(heightInput, weightInput, bmiInput) {
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
}

/**
 * Собирает данные из формы
 * @param {HTMLFormElement} form - Элемент формы
 * @param {string} currentLang - Текущий язык
 * @returns {Object} Данные формы
 */
export function collectFormData(form, currentLang) {
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload.ui_language = currentLang;
    return payload;
}

/**
 * Блокирует форму во время отправки
 * @param {HTMLFormElement} form - Элемент формы
 * @param {boolean} disabled - Заблокировать или разблокировать
 */
export function setFormDisabled(form, disabled) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = disabled;
        if (disabled) {
            submitButton.dataset.originalText = submitButton.textContent;
            submitButton.textContent = "Processing...";
        } else {
            submitButton.textContent = submitButton.dataset.originalText || "Assess Risk";
        }
    }
}

/**
 * Сбрасывает состояние формы
 * @param {HTMLFormElement} form - Элемент формы
 */
export function resetFormState(form) {
    // Удаляем только error-warning
    document.querySelectorAll(".error-warning").forEach(el => el.remove());

    // Сбрасываем patient report
    const patient = document.querySelector(".patient-report");
    if (patient) {
        patient.style.display = "none";
    }

    // НЕ скрываем doctor report - он должен быть всегда виден
    const doctor = document.querySelector(".doctor-report");
    if (doctor) {
        doctor.style.display = "block";
        
        doctor.querySelectorAll("[data-section] ul").forEach(ul => {
            ul.innerHTML = "<li>—</li>";
        });

        doctor.querySelectorAll("[data-section] p").forEach(p => {
            if (!p.closest("[data-section='disclaimer']")) {
                p.textContent = "—";
            }
        });
    }
}


