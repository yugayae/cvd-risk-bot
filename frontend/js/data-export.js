/**
 * Data Export Utility
 * Handles generation and download of CSV and JSON files for patient data.
 */

/**
 * Maps risk category to human-readable format for CSV
 * @param {string} cat 
 * @returns {string}
 */
function formatCategory(cat) {
    return cat ? cat.charAt(0).toUpperCase() + cat.slice(1) : 'Unknown';
}

/**
 * Triggers a browser download for a blob
 * @param {Blob} blob 
 * @param {string} filename 
 */
function triggerDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

/**
 * Generates and downloads a CSV file based on the 14-column clinical standard.
 * @param {Object} resultData 
 * @param {FormData|Object} formData 
 */
export function exportToCSV(resultData, formData) {
    const getValue = (key) => (formData instanceof FormData ? formData.get(key) : formData[key]) || 'N/A';

    // 14 Columns Clinical Standard
    const headers = [
        'Date', 'Region', 'Age', 'Sex', 'SystolicBP', 'DiastolicBP',
        'Cholesterol', 'Glucose', 'BMI', 'Smoking', 'Alcohol',
        'PhysicalActivity', 'RiskProbability', 'RiskCategory'
    ];

    const row = [
        new Date().toISOString().split('T')[0],
        getValue('region') || 'unknown',
        getValue('age_years'),
        parseInt(getValue('gender')) === 2 ? 'Male' : 'Female',
        getValue('ap_hi'),
        getValue('ap_lo'),
        getValue('cholesterol'),
        getValue('gluc'),
        resultData.patient_bmi ? resultData.patient_bmi.toFixed(2) : 'N/A',
        parseInt(getValue('smoke')) === 1 ? 'Yes' : 'No',
        parseInt(getValue('alco')) === 1 ? 'Yes' : 'No',
        parseInt(getValue('active')) === 1 ? 'Yes' : 'No',
        `${(resultData.risk_probability * 100).toFixed(1)}%`,
        formatCategory(resultData.risk_category)
    ];

    const csvContent = [headers.join(','), row.join(',')].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

    triggerDownload(blob, `CVD_Report_${timestamp}.csv`);
}

/**
 * Generates and downloads a JSON file of the prediction result.
 * @param {Object} resultData 
 */
export function exportToJSON(resultData) {
    const jsonContent = JSON.stringify(resultData, null, 2);
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);

    triggerDownload(blob, `CVD_Analysis_${timestamp}.json`);
}
