# Research Note – Future Model Development (v2+)

## 1. Purpose of Data Collection

The current version of the system (v1) may collect anonymized user input data
with explicit user consent. The primary purpose of this data collection is
to support future research and model improvement.

The collected data does NOT affect predictions in the current version.

---

## 2. Current Model Scope (v1)

- The current model is trained on an external, static dataset.
- It does not adapt or retrain based on incoming user data.
- No online learning or real-time personalization is performed.
- User consent does not influence prediction outcomes.

The system functions as a fixed Clinical Decision Support System (CDSS).

---

## 3. Planned Use of Collected Data (v2)

In future versions of the model (v2+), the collected anonymized data may be used for:

- Model recalibration and validation on real-world inputs
- Analysis of feature distributions across regions
- Evaluation of potential regional or demographic bias
- Development of region-aware or population-aware models
- Research and educational publications

Any such use will be performed **offline** and only on consented data.

---

## 4. Planned Model Changes

Potential future enhancements may include:
- Introduction of regional context as a categorical feature
- Improved risk calibration by population subgroup
- Better uncertainty estimation and confidence stratification

No changes will be deployed without prior validation and documentation.

---

## 5. Ethical and Governance Principles

The project follows key principles inspired by:
- WHO Ethics and Governance of AI for Health
- Transparency and informed consent
- Data minimization and anonymization
- Separation between data collection and model inference

---

## 6. Non-Goals

The following are explicitly NOT planned:
- Real-time model retraining on user data
- Individual-level personalization
- Automated clinical decision-making
- Commercial use of collected data

---

## 7. Versioning Commitment

All major model changes will be versioned and documented.
Users will always be informed when a new model version is introduced.

