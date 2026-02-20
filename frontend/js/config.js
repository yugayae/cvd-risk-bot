/**
 * Frontend Configuration
 * Environment-specific settings
 */

export const CONFIG = {
    // API Configuration
    api: {
        baseUrl: typeof window !== 'undefined'
            ? (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                ? `http://${window.location.hostname}:8000`
                : window.location.origin)
            : 'http://localhost:8000',
        timeout: 30000, // 30 seconds
        retryAttempts: 2,
    },

    // Application Configuration
    app: {
        defaultLanguage: 'en',
        supportedLanguages: ['en', 'ru', 'kr'],
        appName: 'CardioRisk AI',
        version: '1.0.0',
    },

    // Clinical Settings
    clinical: {
        // Risk thresholds
        riskThresholds: {
            low: 0.15,      // < 15%
            moderate: 0.40, // 15-40%
            high: 1.0       // > 40%
        },

        // Confidence levels
        confidenceThresholds: {
            high: 0.85,
            moderate: 0.70,
            low: 0
        },

        // Model scope (training data ranges)
        modelScope: {
            age: { min: 40, max: 75 },
            bmi: { min: 18.5, max: 30 },
            systolic: { min: 90, max: 180 },
            diastolic: { min: 60, max: 110 },
            cholesterol: [1, 2, 3], // Categorical
            glucose: [1, 2, 3]      // Categorical
        }
    },

    // UI Configuration
    ui: {
        animationDuration: 300, // ms
        chartAnimationDuration: 1000, // ms
        colors: {
            primary: '#4F46E5',
            primaryHover: '#4338CA',
            secondary: '#10B981',
            danger: '#EF4444',
            warning: '#F59E0B',
            success: '#10B981'
        }
    },

    // Feature Flags
    features: {
        enablePrintReport: true,
        enableExportJSON: true,
        enablePDF: true,
        enableShapExplanation: true,
        enableClinicalWarnings: true,
    },

    // Logging
    logging: {
        enabled: true,
        level: 'debug', // 'debug', 'info', 'warn', 'error'
        persistLogs: false
    }
};

/**
 * Get API URL with optional path
 */
export function getApiUrl(path = '') {
    const baseUrl = CONFIG.api.baseUrl;
    // Ensure all API calls go to /api/
    const apiPath = path.startsWith('/api') ? path : `/api${path.startsWith('/') ? path : '/' + path}`;
    return `${baseUrl}${apiPath}`;
}

/**
 * Check if in development mode
 */
export function isDevelopment() {
    return window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1';
}

/**
 * Log function respecting logging configuration
 */
export function log(message, level = 'debug', data = null) {
    if (!CONFIG.logging.enabled) return;

    const timestamp = new Date().toISOString();
    const levelStr = level.toUpperCase();

    const logEntry = {
        timestamp,
        level,
        message,
        data,
        isDev: isDevelopment()
    };

    // Console output
    if (level === 'error') {
        console.error(`[${timestamp}] ${levelStr}: ${message}`, data);
    } else if (level === 'warn') {
        console.warn(`[${timestamp}] ${levelStr}: ${message}`, data);
    } else if (CONFIG.logging.level === 'debug') {
        console.log(`[${timestamp}] ${levelStr}: ${message}`, data);
    }

    // Optional: Send to server for persistent logging
    if (CONFIG.logging.persistLogs && level === 'error') {
        // TODO: Implement server-side logging
    }
}

export default CONFIG;
