## Intended Use

This tool is intended to support cardiovascular risk assessment in adult
primary care patients (≥18 years) without known cardiovascular disease.

The model provides a probabilistic estimate of cardiovascular risk
to assist clinical decision-making. It does not establish a diagnosis
and does not replace professional medical judgment.

## Target Population

- Adult patients (≥18 years)
- Primary care setting
- No established cardiovascular disease
- Routine clinical data available

### Exclusion Criteria

- Acute cardiovascular events
- Emergency or ICU patients
- Pregnancy
- Rare metabolic or genetic disorders

## Model Overview

The system uses a calibrated logistic regression model trained on
routinely collected clinical variables, including demographics,
blood pressure, anthropometric measures, and lifestyle factors.

Model outputs are calibrated probabilities rather than binary predictions.

## Model Performance

The model's performance metrics are calculated on an independent validation dataset:

- **ROC-AUC**: 0.800 (overall discrimination ability)
- **PR-AUC**: 0.780 (precision-recall balance)
- **Sensitivity (Recall)**: 95.5% (ability to identify high-risk patients)
- **Specificity**: 77.3% (ability to identify low-risk patients)
- **Precision**: 56.0% (positive predictive value)
- **F1-Score**: 70.6% (harmonic mean of precision and recall)
- **Brier Score**: 0.181 (calibration quality, lower is better)
- **Gender-specific ROC-AUC**:
  - Female: 0.806
  - Male: 0.793

These metrics indicate moderate-to-good discrimination with reliable risk calibration. The model prioritizes sensitivity to minimize missed high-risk cases.

### Interpretation Guidelines Based on Metrics

- **High sensitivity (95.5%)** ensures few false negatives, making it suitable for screening
- **Moderate specificity (77.3%)** may result in some false positives, requiring clinical judgment
- **Brier score < 0.2** indicates good probability calibration
- SHAP explanations should be interpreted cautiously when model confidence is low or inputs are near decision boundaries

## Explainability and Safety

Model predictions are accompanied by:
- Clinically interpretable risk factors
- Confidence level estimation
- Input sanity checks
- Out-of-distribution detection
- Explicit clinical safety warnings

These features are designed to reduce misinterpretation and overreliance
on automated predictions.

## Known Limitations

- Reduced reliability near clinical decision thresholds
- Limited performance for extreme values outside the training distribution
- Does not incorporate laboratory or imaging biomarkers
- Not validated for emergency clinical decision-making

## Clinical Workflow Integration

The tool is intended for use after routine clinical measurements
and before treatment decisions, as a decision support aid.

## Regulatory and Ethical Considerations

This system is designed as a clinical decision support tool and
does not provide diagnostic or therapeutic recommendations.

Final clinical decisions remain the responsibility of the healthcare provider.

