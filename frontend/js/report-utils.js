/**
 * Utility for exporting medical reports (PDF/Print)
 */
import { i18n } from './i18n.js';

/**
 * Prepares and triggers the print dialog for a professional medical report
 * @param {Object} data - Prediction response from backend
 * @param {FormData} formData - Original form data
 */
export function printMedicalReport(data, formData) {
    const reportContainer = document.getElementById('medical-report-template');
    if (!reportContainer) {
        console.error('Report template container not found');
        return;
    }

    // Fill the template
    fillReportTemplate(reportContainer, data, formData);

    // Trigger print
    window.print();
}

/**
 * Fills the hidden report template with actual patient data and results
 */
function fillReportTemplate(container, data, formData) {
    const now = new Date();
    const timestamp = now.toLocaleString(i18n.getLanguage() === 'ru' ? 'ru-RU' : 'en-GB');

    // Extract patient info safely
    const getValue = (key) => (formData instanceof FormData ? formData.get(key) : formData[key]);

    const age = getValue('age_years') || '—';
    const genderVal = getValue('gender');
    const gender = parseInt(genderVal) === 2 ? i18n.t('option_male') : i18n.t('option_female');
    const height = getValue('height') || '—';
    const weight = getValue('weight') || '—';
    const ap_hi = getValue('ap_hi') || '—';
    const ap_lo = getValue('ap_lo') || '—';

    // Localization for cholesterol/glucose
    const getLevelText = (val) => {
        const v = parseInt(val);
        if (v === 1) return i18n.t('option_normal');
        if (v === 2) return i18n.t('option_above_normal');
        if (v === 3) return i18n.t('option_high');
        return '—';
    };

    const cholesterol = getLevelText(getValue('cholesterol'));
    const glucose = getLevelText(getValue('gluc'));
    const bmi = data.patient_bmi ? data.patient_bmi.toFixed(1) : '—';

    const riskPercent = Math.round((data.risk_probability || 0) * 100);
    const riskLabel = data.risk_label || i18n.t(`risk_${data.risk_category || 'moderate'}`);

    container.innerHTML = `
        <div class="print-report">
            <div class="report-header">
                <h1>${i18n.t('logo_text')}</h1>
                <div class="report-meta">
                    <div><strong>${i18n.t('header_title')}</strong></div>
                    <div>${timestamp}</div>
                </div>
            </div>

            <section class="report-section">
                <h2>1. ${i18n.t('results_patient_profile')}</h2>
                <table class="report-table">
                    <tr><td>${i18n.t('label_age')}:</td><td>${age}</td></tr>
                    <tr><td>${i18n.t('label_gender')}:</td><td>${gender}</td></tr>
                    <tr><td>${i18n.t('label_height')} / ${i18n.t('label_weight')}:</td><td>${height} cm / ${weight} kg</td></tr>
                    <tr><td>${i18n.t('label_bmi')}:</td><td>${bmi} kg/m²</td></tr>
                </table>
            </section>

            <section class="report-section">
                <h2>2. ${i18n.t('section_indicators')}</h2>
                <table class="report-table">
                    <tr><td>${i18n.t('label_systolic')} / ${i18n.t('label_diastolic')}:</td><td>${ap_hi} / ${ap_lo} mmHg</td></tr>
                    <tr><td>${i18n.t('label_cholesterol')}:</td><td>${cholesterol}</td></tr>
                    <tr><td>${i18n.t('label_glucose')}:</td><td>${glucose}</td></tr>
                </table>
            </section>

            <section class="report-section risk-summary">
                <h2>3. ${i18n.t('results_title')}</h2>
                <div class="risk-result">
                    <div class="risk-value">${riskPercent}%</div>
                    <div class="risk-label">${riskLabel}</div>
                </div>
                <p><strong>${i18n.t('confidence_high')}:</strong> ${data.confidence_title || '--'} (${data.confidence_level || '--'})</p>
                <p class="disclaimer">${data.disclaimer || ''}</p>
            </section>

            <section class="report-section">
                <h2>4. ${i18n.t('results_key_factors')}</h2>
                <ul class="factor-list">
                    ${(data.clinical_explanation || []).map(exp => `
                        <li>
                            <strong>${exp.factor}</strong>: ${exp.clinical_note}
                        </li>
                    `).join('')}
                </ul>
            </section>

            <section class="report-section">
                <h2>5. ${i18n.t('results_recommendations')}</h2>
                <div class="recommendation-box">
                    ${i18n.t(`rec_${data.risk_category || 'moderate'}`)}
                </div>
            </section>

            <div class="report-footer">
                <p>Request ID: ${data.audit?.request_id || 'N/A'} | Model: v${data.audit?.model_version || '1.0'}</p>
                <p style="margin-top: 0.5rem; color: #1e293b; font-weight: 600;">${i18n.t('clinical_disclaimer_detailed')}</p>
            </div>
        </div>
    `;
}
