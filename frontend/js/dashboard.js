/**
 * Dashboard Controller
 * Main application logic for CVD risk assessment UI
 */

import { i18n } from './i18n.js';
import { getPrediction, healthCheck, logPatientData } from './api-service.js';
import CONFIG, { log } from './config.js';
import { printMedicalReport } from './report-utils.js';
import { exportToCSV, exportToJSON } from './data-export.js';

// Global state to store the last result and form data for export
let lastResult = null;
let lastFormData = null;

console.log('[Dashboard] Module loaded');

/**
 * Error Handler Utility
 * Centralized error handling and logging
 */
class ErrorHandler {
    static handle(error, context = 'Unknown') {
        log(`Error in ${context}`, 'error', error);

        // Determine error type
        if (error instanceof TypeError) {
            return {
                message: i18n.t('error_calculation'),
                type: 'type_error',
                details: error.message
            };
        } else if (error instanceof SyntaxError) {
            return {
                message: i18n.t('error_calculation'),
                type: 'syntax_error',
                details: error.message
            };
        } else if (error.message && error.message.includes('network')) {
            return {
                message: i18n.t('error_network'),
                type: 'network_error',
                details: error.message
            };
        } else if (error.message && error.message.includes('timeout')) {
            return {
                message: i18n.t('error_network'),
                type: 'timeout_error',
                details: 'Request timed out'
            };
        } else {
            return {
                message: error.message || i18n.t('error_calculation'),
                type: 'unknown_error',
                details: error.toString()
            };
        }
    }

    static showAlert(errorObj) {
        console.warn(`[${errorObj.type}] ${errorObj.message}`, errorObj.details);
        alert(`${errorObj.message}\n\n${i18n.t('error_api_failed')}`);
    }
}

/**
 * Initialize dashboard
 */
export class Dashboard {
    constructor() {
        try {
            console.log('[Dashboard] Initializing constructor');
            this.form = document.getElementById('risk-form');
            this.submitBtn = document.getElementById('submit-btn');
            this.spinner = document.getElementById('spinner') || document.querySelector('.spinner');
            this.btnText = document.getElementById('btn-text') || document.querySelector('.btn-text');

            this.emptyState = document.getElementById('empty-state');
            this.resultsContainer = document.getElementById('results-container');
            this.dashboardArea = document.getElementById('dashboard-area');
            this.langSwitcher = document.getElementById('lang-switcher');

            // Modal elements
            this.consentModal = document.getElementById('consent-modal');
            this.acceptBtn = document.getElementById('consent-accept');
            this.declineBtn = document.getElementById('consent-decline');

            // Chart instances
            this.gaugeChartInstance = null;
            this.radarChartInstance = null;
            this.shapChartInstance = null;

            this.init();
        } catch (e) {
            console.error('[Dashboard] Constructor failed:', e);
            log('Safe initialization failed', 'error', e);
        }
    }

    init() {
        if (!this.form) return; // Guard clause

        // Event listeners
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.langSwitcher.addEventListener('change', (e) => this.handleLanguageChange(e));

        this.setupHints();
        this.setupLiveBMI();

        const savePdfBtn = document.getElementById('save-pdf-btn');
        const printReportBtn = document.getElementById('print-report-btn');

        // Print handled via printMedicalReport

        if (printReportBtn) {
            printReportBtn.addEventListener('click', () => {
                if (lastResult && lastFormData) {
                    printMedicalReport(lastResult, lastFormData);
                } else {
                    alert(i18n.t('results_empty'));
                }
            });
        }

        const exportCsvBtn = document.getElementById('export-csv-btn');
        const exportJsonBtn = document.getElementById('export-json-btn');

        if (exportCsvBtn) {
            exportCsvBtn.addEventListener('click', () => {
                if (lastResult && lastFormData) {
                    exportToCSV(lastResult, lastFormData);
                } else {
                    alert(i18n.t('results_empty'));
                }
            });
        }

        if (exportJsonBtn) {
            exportJsonBtn.addEventListener('click', () => {
                if (lastResult) {
                    exportToJSON(lastResult);
                } else {
                    alert(i18n.t('results_empty'));
                }
            });
        }

        // Modal Action Listeners
        if (this.acceptBtn) {
            this.acceptBtn.addEventListener('click', () => this.handleConsent(true));
        }
        if (this.declineBtn) {
            this.declineBtn.addEventListener('click', () => this.handleConsent(false));
        }

        // Apply translations
        // Set initial language from browser or default
        try {
            const browserLang = navigator.language.split('-')[0];
            if (['en', 'ru', 'kr'].includes(browserLang)) {
                i18n.setLanguage(browserLang);
                this.langSwitcher.value = browserLang;
                log(`Browser language detected: ${browserLang}`, 'debug');
            } else {
                log(`Browser language not supported: ${browserLang}, using default`, 'warn');
            }
        } catch (error) {
            log('Error detecting browser language', 'warn', error);
            i18n.setLanguage('en');
        }

        // Check backend health
        this.checkBackendHealth();
    }

    /**
     * Check if backend is available
     */
    async checkBackendHealth() {
        try {
            const health = await healthCheck();
            if (health && health.status === 'ok') {
                log('Backend health check passed', 'debug');
            } else {
                log('Backend health check warning: Unexpected response', 'warn', health);
            }
        } catch (error) {
            const errorObj = ErrorHandler.handle(error, 'Backend Health Check');
            log(`Backend connection failed: ${errorObj.message}`, 'warn', errorObj.details);
        }
    }

    /**
     * Handle form submission
     */
    async handleSubmit(e) {
        e.preventDefault();

        // Validate form
        if (!this.form.checkValidity()) {
            alert(i18n.t('error_form_invalid'));
            return;
        }

        console.log('[Dashboard] handleSubmit triggered');

        // UI Loading State
        if (this.submitBtn) this.submitBtn.disabled = true;
        if (this.btnText) this.btnText.style.opacity = '0';
        if (this.spinner) this.spinner.style.display = 'block';

        const formData = new FormData(this.form);

        try {
            // Get prediction from backend
            const result = await getPrediction(formData);

            // Validate response
            if (!result || result.risk_probability === undefined) {
                throw new Error('Invalid prediction response structure');
            }

            // Try to render dashboard with error protection
            try {
                // Save for export
                lastResult = result;
                lastFormData = formData;

                this.renderDashboard(result, formData);

                // Show results
                this.emptyState.style.display = 'none';
                this.resultsContainer.style.display = 'grid'; // Ensure grid layout

                // Scroll to results on mobile
                if (window.innerWidth <= 1024) {
                    this.resultsContainer.scrollIntoView({ behavior: 'smooth' });
                }

                log('Prediction successful', 'info', { risk_probability: result.risk_probability });

                // Show Consent Modal after results are visible
                setTimeout(() => {
                    if (this.consentModal) {
                        this.consentModal.classList.add('active');
                        this.consentModal.style.display = 'flex';
                    }
                }, 1000);

            } catch (renderError) {
                const errorObj = ErrorHandler.handle(renderError, 'Dashboard Rendering');
                ErrorHandler.showAlert(errorObj);
                this.resultsContainer.style.display = 'none';
                this.emptyState.style.display = 'flex';
            }

        } catch (error) {
            const errorObj = ErrorHandler.handle(error, 'Form Submission');
            ErrorHandler.showAlert(errorObj);
            this.resultsContainer.style.display = 'none';
            this.emptyState.style.display = 'flex';
        } finally {
            // Reset UI
            this.submitBtn.disabled = false;
            this.btnText.style.opacity = '1';
            this.spinner.style.display = 'none';
        }
    }

    /**
     * Handle language change
     */
    handleLanguageChange(e) {
        try {
            const lang = e.target.value;
            if (!lang) {
                throw new Error('Invalid language selection');
            }
            i18n.setLanguage(lang);
            this.updateUILanguage();
            log(`Language changed to: ${lang}`, 'debug');

            // Update hints for new language
            const cholSelect = document.getElementById('cholesterol-select');
            const glucSelect = document.getElementById('gluc-select');
            if (cholSelect) this.updateHint('cholesterol', cholSelect.value);
            if (glucSelect) this.updateHint('gluc', glucSelect.value);

        } catch (error) {
            log(`Language change error: ${error.message}`, 'error', error);
            alert(i18n.t('error_calculation'));
        }
    }

    /**
     * Update UI text based on current language
     */
    updateUILanguage() {
        try {
            // Update button text
            if (this.btnText) {
                this.btnText.textContent = i18n.t('btn_assess');
            }

            // Update empty state
            const emptyTitle = this.emptyState?.querySelector('h2');
            const emptyText = this.emptyState?.querySelector('p');
            if (emptyTitle) emptyTitle.textContent = i18n.t('results_title');
            if (emptyText) emptyText.textContent = i18n.t('results_empty');

            // Update form labels
            document.querySelectorAll('[data-i18n]').forEach(el => {
                try {
                    const key = el.getAttribute('data-i18n');
                    if (key) {
                        el.textContent = i18n.t(key);
                    }
                } catch (e) {
                    log(`Error translating element with key: ${el.getAttribute('data-i18n')}`, 'warn', e);
                }
            });

            log('UI language updated successfully', 'debug');
        } catch (error) {
            log(`UI language update error: ${error.message}`, 'error', error);
        }
    }

    /**
     * Render dashboard with prediction results
     */
    renderDashboard(data, formData) {
        const probability = data.risk_probability || 0;
        const percent = Math.round(probability * 100);
        const riskCategory = (data.risk_category || 'moderate').toLowerCase();

        // Get color based on risk category
        let color, label;
        if (riskCategory === 'low') {
            color = '#10B981'; // Emerald 500
            label = i18n.t('risk_low');
        } else if (riskCategory === 'moderate') {
            color = '#F59E0B'; // Amber 500
            label = i18n.t('risk_moderate');
        } else {
            color = '#f43f5e'; // Rose 500
            label = i18n.t('risk_high');
        }

        // Update main score card
        const riskBadge = document.getElementById('risk-percent');
        const riskLabel = document.getElementById('risk-category');
        const mainCard = document.querySelector('.card-score');

        if (riskBadge) {
            riskBadge.innerText = `${percent}%`;
            riskBadge.style.background = `-webkit-linear-gradient(45deg, ${color}, #111827)`;
            riskBadge.style.webkitBackgroundClip = 'text';
            riskBadge.style.webkitTextFillColor = 'transparent';
        }

        if (riskLabel) {
            riskLabel.innerText = label;
            riskLabel.style.color = color;
        }

        if (mainCard) {
            mainCard.style.borderLeftColor = color;
        }

        // Update BMI
        const bmiValue = document.getElementById('bmi-value');
        if (bmiValue && data.patient_bmi) {
            bmiValue.innerText = data.patient_bmi.toFixed(1);
        }

        // Render Recommendations (Second Opinion)
        const recContent = document.getElementById('recommendation-content');
        if (recContent) {
            recContent.innerHTML = `
                <div class="recommendation-box" style="border-left: 4px solid ${color}">
                    <p>${i18n.t('rec_' + riskCategory)}</p>
                </div>
            `;

            // Add clinical explanations if available
            if (data.clinical_explanation && data.clinical_explanation.length > 0) {
                const ul = document.createElement('ul');
                ul.style.listStyle = 'none';
                ul.style.paddingLeft = '0';
                ul.style.marginTop = '1rem';

                const header = document.createElement('li');
                header.innerHTML = `<strong>${i18n.t('results_key_factors')}:</strong>`;
                header.style.marginBottom = '0.5rem';
                ul.appendChild(header);

                data.clinical_explanation.forEach(item => {
                    const li = document.createElement('li');
                    li.style.marginBottom = '0.4rem';
                    li.style.fontSize = '0.9rem';
                    li.innerHTML = `<span style="font-weight:600; color:${color}">${item.factor}</span>: ${item.clinical_note}`;
                    ul.appendChild(li);
                });
                recContent.appendChild(ul);
            }
        }

        // Render CDSS Disclaimer
        const disclaimerBox = document.getElementById('clinical-disclaimer-box');
        if (disclaimerBox) {
            disclaimerBox.textContent = i18n.t('clinical_disclaimer_detailed');
        }

        // Destroy old charts
        this.destroyCharts();

        // Render new charts
        this.renderCharts(probability, percent, color, data, formData);

        // Trigger animations
        document.querySelectorAll('.card').forEach(card => {
            card.classList.remove('visible');
            void card.offsetWidth; // trigger reflow
            card.classList.add('visible');
        });
    }

    /**
     * Destroy existing chart instances
     */
    destroyCharts() {
        if (this.gaugeChartInstance) this.gaugeChartInstance.destroy();
        if (this.radarChartInstance) this.radarChartInstance.destroy();
        if (this.shapChartInstance) this.shapChartInstance.destroy();
    }

    /**
     * Render all charts with error protection
     */
    renderCharts(probability, percent, color, data, formData) {
        try {
            // Common Chart Options
            const commonOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#1e293b',
                        bodyColor: '#475569',
                        borderColor: '#e2e8f0',
                        borderWidth: 1,
                        padding: 10,
                        cornerRadius: 8,
                        displayColors: false
                    }
                }
            };

            this.renderGaugeChart(percent, color, commonOptions);
            this.renderRadarChart(formData, commonOptions);
            this.renderShapChart(data, color, commonOptions);

        } catch (error) {
            const errorObj = ErrorHandler.handle(error, 'Chart Rendering Process');
            log(`Chart rendering process error: ${errorObj.message}`, 'error', errorObj.details);
        }
    }

    /**
     * Render Gauge (Doughnut) Chart
     */
    renderGaugeChart(percent, color, common) {
        try {
            const ctxGauge = document.getElementById('gaugeChart');
            if (!ctxGauge) return;

            this.gaugeChartInstance = new Chart(ctxGauge.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: [i18n.t('chart_risk'), i18n.t('chart_safe')],
                    datasets: [{
                        data: [percent, 100 - percent],
                        backgroundColor: [color, 'rgba(0,0,0,0.05)'],
                        borderWidth: 0,
                        borderRadius: 20,
                        cutout: '85%'
                    }]
                },
                options: {
                    ...common,
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    }
                }
            });
        } catch (error) { log('Gauge chart error', 'error', error); }
    }

    /**
     * Render Radar Chart
     */
    renderRadarChart(formData, common) {
        try {
            const ctxRadar = document.getElementById('radarChart');
            if (!ctxRadar) return;

            const age = parseInt(formData.get('age_years')) || 45;

            const ap_hi = parseInt(formData.get('ap_hi')) || 120;
            const cholesterol = parseInt(formData.get('cholesterol')) || 1;
            const gluc = parseInt(formData.get('gluc')) || 1;

            // Calculate BMI for chart
            const height = parseInt(formData.get('height')) || 175;
            const weight = parseFloat(formData.get('weight')) || 70;
            const bmi = weight / ((height / 100) ** 2) || 24;

            this.radarChartInstance = new Chart(ctxRadar.getContext('2d'), {
                type: 'radar',
                data: {
                    labels: [
                        i18n.t('shap_age'),
                        i18n.t('shap_systolic'),
                        i18n.t('shap_cholesterol'),
                        i18n.t('shap_glucose'),
                        i18n.t('shap_bmi')
                    ],
                    datasets: [{
                        label: 'Patient Profile',
                        data: [
                            Math.min((age / 100) * 100, 100),
                            Math.min((ap_hi / 200) * 100, 100),
                            cholesterol * 33,
                            gluc * 33,
                            Math.min((bmi / 40) * 100, 100)
                        ],
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        borderColor: '#6366f1',
                        borderWidth: 2,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#6366f1',
                        pointHoverBackgroundColor: '#6366f1',
                        pointHoverBorderColor: '#fff'
                    }]
                },
                options: {
                    ...common,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(0,0,0,0.05)' },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            pointLabels: {
                                font: { size: 11, family: 'Inter' },
                                color: '#64748b'
                            },
                            suggestedMin: 0,
                            suggestedMax: 100,
                            ticks: { display: false }
                        }
                    }
                }
            });
        } catch (error) { log('Radar chart error', 'error', error); }
    }

    /**
     * Render SHAP Bar Chart
     */
    renderShapChart(data, color, common) {
        try {
            const ctxShap = document.getElementById('shapChart');
            if (!ctxShap) return;

            // Extract data
            let chartLabels = [];
            let chartData = [];

            if (data.clinical_explanation && data.clinical_explanation.length > 0) {
                // Limit to top 5 factors
                const topFactors = data.clinical_explanation.slice(0, 5);
                chartLabels = topFactors.map(i => i.factor);
                // Visual representation: simplified magnitude
                chartData = topFactors.map(i => {
                    if (i.shap_value !== undefined && i.shap_value !== null) {
                        return i.shap_value * 100; // Scale for better visibility
                    }
                    return (i.raw_direction === 'increases' || i.direction === 'increases') ? 75 : -25;
                });
            } else {
                // Fallback
                chartLabels = ['Age', 'Blood Pressure', 'Cholesterol', 'Smoking'];
                chartData = [50, 60, 30, 0];
            }

            this.shapChartInstance = new Chart(ctxShap.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: chartLabels,
                    datasets: [{
                        label: 'Risk Contribution',
                        data: chartData,
                        backgroundColor: chartData.map(v => v > 0 ? '#f43f5e' : '#10b981'),
                        borderRadius: 6,
                        barThickness: 20
                    }]
                },
                options: {
                    ...common,
                    indexAxis: 'y',
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { display: false }
                        },
                        y: {
                            grid: { display: false },
                            ticks: {
                                font: { family: 'Inter', size: 12 },
                                color: '#475569'
                            }
                        }
                    }
                }
            });
        } catch (error) { log('SHAP chart error', 'error', error); }
    }

    /**
     * Handles the user's consent choice for data logging
     * @param {boolean} agreed - Whether the user agreed to data collection
     */
    handleConsent(agreed) {
        if (this.consentModal) {
            this.consentModal.classList.remove('active');
            setTimeout(() => {
                this.consentModal.style.display = 'none';
            }, 300);
        }

        if (agreed && lastResult && lastFormData) {
            const logData = {
                region: lastFormData.get('region') || 'unknown',
                age_years: parseInt(lastFormData.get('age_years')),
                gender: parseInt(lastFormData.get('gender')),
                ap_hi: parseInt(lastFormData.get('ap_hi')),
                ap_lo: parseInt(lastFormData.get('ap_lo')),
                cholesterol: parseInt(lastFormData.get('cholesterol')),
                gluc: parseInt(lastFormData.get('gluc')),
                bmi: lastResult.patient_bmi,
                smoke: parseInt(lastFormData.get('smoke')),
                alco: parseInt(lastFormData.get('alco')),
                active: parseInt(lastFormData.get('active')),
                risk_probability: (lastResult.risk_probability * 100).toFixed(1),
                risk_category: lastResult.risk_category
            };

            logPatientData(logData).then(resp => {
                log('GSheets Logging Response:', 'debug', resp);
            }).catch(err => {
                log('Logging Error:', 'error', err);
            });
        }
    }

    /**
     * Update clinical hints based on selection
     */
    setupHints() {
        const cholSelect = document.getElementById('cholesterol-select');
        const glucSelect = document.getElementById('gluc-select');

        if (cholSelect) {
            cholSelect.addEventListener('change', () => this.updateHint('cholesterol', cholSelect.value));
            // Trigger initial state
            this.updateHint('cholesterol', cholSelect.value);
        }

        if (glucSelect) {
            glucSelect.addEventListener('change', () => this.updateHint('gluc', glucSelect.value));
            // Trigger initial state
            this.updateHint('gluc', glucSelect.value);
        }
    }

    updateHint(type, value) {
        const containerId = type === 'cholesterol' ? 'cholesterol-hint' : 'gluc-hint';
        const container = document.getElementById(containerId);
        if (!container) return;

        const textEl = container.querySelector('.hint-text');

        const statusKeyMap = { '1': 'normal', '2': 'above_normal', '3': 'high' };
        const statusKey = statusKeyMap[value];
        const statusText = i18n.t(`option_${statusKey}`);

        const refKey = `ref_${type === 'cholesterol' ? 'cholesterol' : 'glucose'}_${value}`;
        const hintKey = `hint_${type === 'cholesterol' ? 'cholesterol' : 'glucose'}_${value}`;

        const refValue = i18n.t(refKey);
        const clinicalHint = i18n.t(hintKey);

        const feedback = i18n.t('hint_selection_feedback')
            .replace('{status}', statusText)
            .replace('{value}', refValue);

        textEl.innerHTML = `
            <div style="margin-bottom: 0.25rem;"><strong>${feedback}</strong></div>
            <div style="font-style: italic; opacity: 0.9;">${clinicalHint}</div>
        `;

        container.style.display = 'block';
    }

    /**
     * Set up real-time BMI calculation in sidebar
     */
    setupLiveBMI() {
        const heightInput = document.getElementById('height');
        const weightInput = document.getElementById('weight');

        if (heightInput && weightInput) {
            const updateFn = () => this.updateLiveBMI(heightInput.value, weightInput.value);
            heightInput.addEventListener('input', updateFn);
            weightInput.addEventListener('input', updateFn);

            // Initial calculation
            this.updateLiveBMI(heightInput.value, weightInput.value);
        }
    }

    updateLiveBMI(height, weight) {
        const h = parseFloat(height) / 100;
        const w = parseFloat(weight);
        const container = document.getElementById('live-bmi-container');
        const valueEl = document.getElementById('live-bmi-value');

        if (h > 0 && w > 0) {
            const bmi = (w / (h * h)).toFixed(1);
            if (valueEl) valueEl.textContent = bmi;
            if (container) container.style.display = 'inline-block';
        } else {
            if (container) container.style.display = 'none';
        }
    }
}

// Initialize on DOM load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.dashboard = new Dashboard();
    });
} else {
    window.dashboard = new Dashboard();
}

export default Dashboard;
