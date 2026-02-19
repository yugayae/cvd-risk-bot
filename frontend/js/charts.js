/**
 * Модуль для работы с Chart.js графиками
 * Включает Risk Gauge и SHAP Bar Chart
 */

/**
 * Создает диаграмму-калибр для отображения риска
 * @param {string} canvasId - ID canvas элемента
 * @param {number} probability - Вероятность (0-1)
 * @param {string} riskCategory - Категория риска (low, moderate, high)
 * @returns {Chart|null} Chart instance или null если элемент не найден
 */
export function createRiskGaugeChart(canvasId, probability, riskCategory = 'moderate') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`[Risk Gauge] Canvas with id "${canvasId}" not found`);
        return null;
    }

    console.log(`[Risk Gauge] Canvas found:`, {
        id: canvasId,
        size: { width: ctx.width, height: ctx.height },
        offsetSize: { width: ctx.offsetWidth, height: ctx.offsetHeight }
    });

    // Очищаем предыдущий график если он существует
    if (window.chartInstances && window.chartInstances[canvasId]) {
        window.chartInstances[canvasId].destroy();
    }

    const percentage = Math.round(probability * 100);

    // Определяем цвет на основе риска
    const colorMap = {
        low: '#10B981',      // green
        moderate: '#F59E0B', // yellow
        high: '#EF4444'      // red
    };
    const color = colorMap[riskCategory] || '#F59E0B';

    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [
                {
                    data: [percentage, 100 - percentage],
                    backgroundColor: [color, '#E5E7EB'],
                    borderWidth: 0,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            circumference: 180,
            rotation: 270,
            cutout: '75%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function (context) {
                            if (context.dataIndex === 0) {
                                return `Risk: ${percentage}%`;
                            }
                            return null;
                        }
                    }
                }
            }
        },
        plugins: [
            {
                id: 'textCenter',
                beforeDatasetsDraw(chart) {
                    const { ctx, chartArea: { left, top, width, height } } = chart;
                    ctx.save();

                    // Рисуем процент в центре
                    ctx.font = 'bold 32px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = '#2C3E50';
                    ctx.fillText(`${percentage}%`, left + width / 2, top + height / 2 - 10);

                    // Рисуем подпись
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = '#6C7A89';
                    ctx.fillText('Risk', left + width / 2, top + height / 2 + 15);

                    ctx.restore();
                }
            }
        ]
    });

    // Сохраняем ссылку для последущего удаления
    if (!window.chartInstances) {
        window.chartInstances = {};
    }
    window.chartInstances[canvasId] = chart;

    console.log(`[Risk Gauge] Successfully created chart for ${canvasId}`, {
        percentage: Math.round(probability * 100),
        riskCategory,
        chartInstance: !!chart
    });

    return chart;
}

/**
 * Создает горизонтальный bar chart для SHAP факторов
 * @param {string} canvasId - ID canvas элемента
 * @param {Array} shapData - Массив объектов с factor, shap_value, clinical_note
 * @param {number} topN - Количество верхних факторов для отображения
 * @returns {Chart|null} Chart instance или null
 */
export function createShapChart(canvasId, shapData, topN = 5) {
    console.log(`[SHAP Chart] Starting for canvas: ${canvasId}`, { shapData, topN });

    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`[SHAP Chart] Canvas with id "${canvasId}" not found`);
        return null;
    }
    console.log(`[SHAP Chart] Canvas element found:`, ctx);

    // Очищаем предыдущий график
    if (window.chartInstances && window.chartInstances[canvasId]) {
        console.log(`[SHAP Chart] Destroying previous chart instance`);
        window.chartInstances[canvasId].destroy();
    }

    if (!Array.isArray(shapData) || shapData.length === 0) {
        console.warn('[SHAP Chart] Invalid or empty SHAP data', shapData);
        return null;
    }

    // Берем топ N факторов
    const topFactors = shapData.slice(0, topN);
    console.log(`[SHAP Chart] Top ${topN} factors:`, topFactors);

    // Готовим данные
    const labels = topFactors.map(item => item.factor || 'Unknown');
    const values = topFactors.map(item => Math.abs(item.shap_value || 0));

    console.log(`[SHAP Chart] Labels:`, labels);
    console.log(`[SHAP Chart] Values:`, values);

    // Определяем цвета на основе SHAP значений
    const colors = topFactors.map(item => {
        const val = item.shap_value || 0;
        // Красный если повышает риск, Зеленый если снижает
        return val > 0 ? '#EF4444' : '#10B981';
    });

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'SHAP Impact',
                    data: values,
                    backgroundColor: colors,
                    borderRadius: 4,
                    borderSkipped: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 12 },
                    bodyFont: { size: 11 },
                    callbacks: {
                        label: function (context) {
                            const value = context.parsed.x.toFixed(4);
                            return `Impact: ${value}`;
                        },
                        afterLabel: function (context) {
                            const originalData = topFactors[context.dataIndex];
                            if (originalData.clinical_note) {
                                return `Note: ${originalData.clinical_note}`;
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: Math.max(...values) * 1.2,
                    ticks: {
                        callback: function (value) {
                            return value.toFixed(2);
                        }
                    },
                    title: {
                        display: true,
                        text: 'SHAP Value (Absolute)',
                        font: { size: 11 }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Contributing Factors'
                    }
                }
            }
        }
    });

    if (!window.chartInstances) {
        window.chartInstances = {};
    }
    window.chartInstances[canvasId] = chart;

    console.log(`[SHAP Chart] Successfully created chart for ${canvasId}`, chart);

    return chart;
}

/**
 * Создает radar chart для профиля риска
 * @param {string} canvasId - ID canvas элемента
 * @param {Object} payload - Нормализованные данные пациента
 * @returns {Chart|null} Chart instance или null
 */
export function createRadarChart(canvasId, payload) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`[Radar Chart] Canvas with id "${canvasId}" not found`);
        return null;
    }

    // Очищаем предыдущий график
    if (window.chartInstances && window.chartInstances[canvasId]) {
        window.chartInstances[canvasId].destroy();
    }

    // Подготавливаем данные - нормализуем в 0-100
    const radarData = {
        age: Math.min(100, (Number(payload.age_years) / 80) * 100),
        bp: Math.min(100, ((Number(payload.ap_hi) + Number(payload.ap_lo)) / 300) * 100),
        bmi: payload.bmi ? Math.min(100, (Number(payload.bmi) / 35) * 100) : 0,
        cholesterol: (Number(payload.cholesterol) * 33),
        glucose: (Number(payload.gluc) * 33),
        smoking: payload.smoke === 1 || payload.smoke === '1' ? 100 : 0,
        activity: payload.active === 1 || payload.active === '1' ? 100 : 0
    };

    const chart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Age', 'BP', 'BMI', 'Cholesterol', 'Glucose', 'Smoking', 'Activity'],
            datasets: [
                {
                    label: 'Risk Profile',
                    data: Object.values(radarData),
                    borderColor: '#EF4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.15)',
                    borderWidth: 2,
                    pointBackgroundColor: '#EF4444',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${Math.round(context.parsed.r)}%`;
                        }
                    }
                }
            },
            scales: {
                r: {
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        callback: function (value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        }
    });

    if (!window.chartInstances) {
        window.chartInstances = {};
    }
    window.chartInstances[canvasId] = chart;
    console.log(`[Radar Chart] Successfully created for ${canvasId}`);

    return chart;
}

/**
 * Создает диаграмму доверия модели
 * @param {string} canvasId - ID canvas элемента
 * @param {number} confidence - Уровень доверия (0-1)
 * @param {Object} data - Данные предсказания
 * @returns {Chart|null} Chart instance или null
 */
export function createPerformanceChart(canvasId, confidence, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`[Performance Chart] Canvas with id "${canvasId}" not found`);
        return null;
    }

    // Очищаем предыдущий график
    if (window.chartInstances && window.chartInstances[canvasId]) {
        window.chartInstances[canvasId].destroy();
    }

    const confPercent = Math.round(confidence * 100);
    const riskPercent = data.risk_probability ? Math.round(data.risk_probability * 100) : 0;
    const uncertaintyPercent = 100 - confPercent;

    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Confidence', 'Uncertainty'],
            datasets: [
                {
                    data: [confPercent, uncertaintyPercent],
                    backgroundColor: ['#10B981', 'rgba(200, 200, 200, 0.3)'],
                    borderColor: ['#059669', '#D1D5DB'],
                    borderWidth: 2,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '65%',
            plugins: {
                legend: { display: true, position: 'bottom' },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                }
            }
        },
        plugins: [
            {
                id: 'textCenter',
                beforeDatasetsDraw(chart) {
                    const { ctx, chartArea: { left, top, width, height } } = chart;
                    ctx.save();

                    ctx.font = 'bold 24px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = '#10B981';
                    ctx.fillText(`${confPercent}%`, left + width / 2, top + height / 2 - 10);

                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = '#6C7A89';
                    ctx.fillText('Confidence', left + width / 2, top + height / 2 + 15);

                    ctx.restore();
                }
            }
        ]
    });

    if (!window.chartInstances) {
        window.chartInstances = {};
    }
    window.chartInstances[canvasId] = chart;
    console.log(`[Performance Chart] Successfully created for ${canvasId}`);

    return chart;
}
export function destroyAllCharts() {
    if (window.chartInstances) {
        Object.values(window.chartInstances).forEach(chart => {
            if (chart && chart.destroy) {
                chart.destroy();
            }
        });
        window.chartInstances = {};
    }
}

/**
 * Показывает/скрывает charts section
 * @param {boolean} show - Показать или спрятать
 */
export function toggleChartsSection(show = true) {
    const chartsSection = document.querySelector('.charts-section');
    if (chartsSection) {
        const newDisplay = show ? 'block' : 'none';
        chartsSection.style.display = newDisplay;
        console.log(`[Charts Section] Toggled to display: ${newDisplay}`);
    } else {
        console.warn('[Charts Section] Container not found');
    }
}
