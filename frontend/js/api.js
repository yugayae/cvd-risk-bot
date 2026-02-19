/**
 * Модуль для работы с API
 */

import { API_BASE_URL, API_ENDPOINTS } from './constants.js';

/**
 * Выполняет запрос к API для предсказания риска
 * @param {Object} payload - Данные пациента
 * @returns {Promise<Object>} Ответ от API
 */
export async function fetchPrediction(payload) {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.predict}`, {
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
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.health}`);
        return response.ok;
    } catch (error) {
        console.error("API health check failed:", error);
        return false;
    }
}

/**
 * Загружает метрики модели
 * @returns {Promise<Object|null>} Метрики или null
 */
export async function loadModelMetrics() {
    try {
        const metricsUrl = `${API_BASE_URL}${API_ENDPOINTS.metrics}`;
        console.log('[API] Loading model metrics from:', metricsUrl);
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
        
        try {
            const response = await fetch(metricsUrl, {
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const data = await response.json();
                console.log('[API] Model metrics loaded successfully');
                return data;
            } else {
                console.warn('[API] Metrics endpoint returned status:', response.status);
                return null;
            }
        } catch (fetchError) {
            clearTimeout(timeoutId);
            throw fetchError;
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            console.warn('[API] Model metrics request timeout (5s) - ensure API server is running');
        } else if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            console.warn('[API] Failed to fetch model metrics - ensure API server is running at', API_BASE_URL);
        } else {
            console.warn('[API] Error loading model metrics:', error.message);
        }
        return null;
    }
}


