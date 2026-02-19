/**
 * Risk Gauge Animation Module
 * Provides visual risk indicators for patient and doctor interfaces
 */

/**
 * Risk color mapping
 */
const RISK_COLORS = {
    low: '#10b981',      // green
    moderate: '#f59e0b',  // yellow
    high: '#ef4444'       // red
};

/**
 * Create and animate risk gauge for patient
 * @param {number} riskPercent - Risk percentage (0-100)
 * @param {string} riskCategory - Risk category ('low', 'moderate', 'high')
 */
export function animatePatientRiskGauge(riskPercent, riskCategory) {
    const container = document.getElementById('patient-risk-gauge');
    if (!container) {
        console.warn('Patient risk gauge container not found');
        return;
    }

    const color = RISK_COLORS[riskCategory] || '#6b7280';

    // Create gauge HTML
    container.innerHTML = `
        <div class="risk-gauge">
            <div class="risk-gauge-circle" style="
                background: conic-gradient(${color} 0% ${riskPercent}%, #e5e7eb ${riskPercent}% 100%);
            ">
                <div class="risk-gauge-text">
                    <div class="risk-percentage">${riskPercent}%</div>
                    <div class="risk-label">Risk</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Create and animate risk gauge for doctor
 * @param {number} riskPercent - Risk percentage (0-100)
 * @param {string} riskCategory - Risk category ('low', 'moderate', 'high')
 */
export function animateDoctorRiskGauge(riskPercent, riskCategory) {
    const container = document.getElementById('doctor-risk-gauge');
    if (!container) {
        console.warn('Doctor risk gauge container not found');
        return;
    }

    const color = RISK_COLORS[riskCategory] || '#6b7280';

    // Create gauge HTML
    container.innerHTML = `
        <div class="risk-gauge doctor-gauge">
            <div class="risk-gauge-circle" style="
                background: conic-gradient(${color} 0% ${riskPercent}%, #e5e7eb ${riskPercent}% 100%);
            ">
                <div class="risk-gauge-text">
                    <div class="risk-percentage">${riskPercent}%</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Utility function to get risk percentage from probability
 * @param {number} probability - Risk probability (0-1)
 * @returns {number} Risk percentage (0-100)
 */
export function probabilityToPercent(probability) {
    if (typeof probability !== 'number' || isNaN(probability)) {
        return 0;
    }
    return Math.round(probability * 100);
}

/**
 * Utility function to get risk category from probability
 * @param {number} probability - Risk probability (0-1)
 * @returns {string} Risk category
 */
export function getRiskCategory(probability) {
    if (probability < 0.1) return 'low';
    if (probability < 0.2) return 'moderate';
    return 'high';
}