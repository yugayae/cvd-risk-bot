/**
 * Модуль для работы с API
 */

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Выполняет запрос к API для предсказания риска
 * @param {Object} payload - Данные пациента
 * @returns {Promise<Object>} Ответ от API
 */
export async function fetchPrediction(payload) {
    const response = await fetch(`${API_BASE_URL}/predict`, {
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
    
    return raw;
}

/**
 * Проверяет доступность API
 * @returns {Promise<boolean>} true если API доступен
 */
export async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error("API health check failed:", error);
        return false;
    }
}


