/**
 * API Service for backend communication
 * Handles CVD risk prediction requests
 */

import { i18n } from './i18n.js';
import { getApiUrl } from './config.js';

const API_BASE_URL = getApiUrl();

/**
 * Calculate age from Date of Birth
 */
export function calculateAge(dobString) {
    if (!dobString) return 0;
    const dob = new Date(dobString);
    const diff_ms = Date.now() - dob.getTime();
    const age_dt = new Date(diff_ms);
    return Math.abs(age_dt.getUTCFullYear() - 1970);
}

/**
 * Transform frontend form data to backend schema
 */
function transformFormDataToPayload(formData) {
    const dob = formData.get('dob');
    const age = calculateAge(dob);

    return {
        age_years: age,
        height: parseInt(formData.get('height')),
        weight: parseFloat(formData.get('weight')),
        ap_hi: parseInt(formData.get('ap_hi')),
        ap_lo: parseInt(formData.get('ap_lo')),
        cholesterol: parseInt(formData.get('cholesterol')),
        gluc: parseInt(formData.get('gluc')),
        active: parseInt(formData.get('active')),
        smoke: parseInt(formData.get('smoke')),
        alco: parseInt(formData.get('alco')),
        gender: parseInt(formData.get('gender')), // 1=Female, 2=Male
        ui_language: i18n.getLanguage(),
        region: formData.get('region') || 'Unknown'
    };
}

/**
 * Validate payload before sending to backend
 */
function validatePayload(payload) {
    const errors = [];

    if (!payload.age_years || payload.age_years < 18 || payload.age_years > 90) {
        errors.push(i18n.t('error_validation_age') || 'Invalid age (18-90)');
    }
    if (!payload.height || payload.height < 100 || payload.height > 250) {
        errors.push('Invalid height (100-250cm)');
    }
    if (!payload.weight || payload.weight < 30 || payload.weight > 200) {
        errors.push('Invalid weight (30-200kg)');
    }
    if (!payload.ap_hi || payload.ap_hi < 60 || payload.ap_hi > 240) {
        errors.push('Invalid systolic BP (60-240)');
    }
    if (!payload.ap_lo || payload.ap_lo < 40 || payload.ap_lo > 160) {
        errors.push('Invalid diastolic BP (40-160)');
    }
    if (![1, 2, 3].includes(payload.cholesterol)) {
        errors.push('Invalid cholesterol value');
    }

    return {
        isValid: errors.length === 0,
        errors
    };
}

/**
 * Get CVD risk prediction from backend
 * @param {FormData} formData - Form data from the input form
 * @returns {Promise<Object>} Backend response with predictions
 */
export async function getPrediction(formData) {
    try {
        // Transform form data to backend schema
        const payload = transformFormDataToPayload(formData);

        // Validate data
        const validation = validatePayload(payload);
        if (!validation.isValid) {
            throw new Error(`Validation errors: ${validation.errors.join(', ')}`);
        }

        // Make request to backend
        const response = await fetch(getApiUrl('/predict'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();
        return result;

    } catch (error) {
        console.error('Error in getPrediction:', error);
        throw error;
    }
}

/**
 * Get model performance metrics
 */
export async function getModelMetrics() {
    try {
        const response = await fetch(getApiUrl('/metrics'));
        if (!response.ok) {
            throw new Error(`Metrics error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching metrics:', error);
        throw error;
    }
}

/**
 * Health check
 */
export async function healthCheck() {
    try {
        const response = await fetch(getApiUrl('/health'));
        if (!response.ok) throw new Error('Health check failed');
        return await response.json();
    } catch (error) {
        console.error('Health check error:', error);
        return { status: 'error', message: error.message };
    }
}

/**
 * Log patient data to Google Sheets
 * @param {Object} data - Anonymized patient data
 */
export async function logPatientData(data) {
    try {
        const response = await fetch(getApiUrl('/api/log-patient-data'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('Error logging data:', error);
        return { status: 'error', message: error.message };
    }
}

export { API_BASE_URL };
