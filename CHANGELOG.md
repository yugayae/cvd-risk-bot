# Changelog

All notable changes to CVD Risk Predictor documented here.

---

## [1.1.0] - 2025-02-09

### ✨ Added
- **User consent system** for anonymous data collection
- **Google Sheets integration** for research data logging
- **Region selection** for geographic tracking
- **Auto BMI calculation** from height and weight input
- **Quick action buttons** after results (New Analysis / Statistics / Help)
- **Improved user flow** with consent and region questions
- **Enhanced privacy** with transparent data collection practices

### 🔄 Changed
- BMI input → Height & Weight input with automatic calculation
- Added 2 new conversation states (CONSENT, REGION)
- Improved user experience with clearer data collection explanation
- Updated message templates for all 3 languages

### 🔒 Security
- Anonymous data logging (no Telegram ID stored)
- Voluntary consent mechanism
- GDPR-compliant data handling

---

## [1.0.0] - 2025-02-06

### ✨ Added
- Initial release
- Telegram bot interface with multi-language support (ru/en/kr)
- CatBoost ML model for CVD risk prediction
- SHAP explanations for interpretability
- FastAPI backend with async support
- Rate limiting (10 requests/day per user)
- Health check endpoint for monitoring
- Docker deployment configuration
- Render.com deployment support
- Usage statistics tracking
- Comprehensive documentation

### 🔒 Security
- Input validation with Pydantic
- Rate limiting protection
- No data storage (privacy-first)
- Timeout protection

### 📊 Model
- CatBoost classifier with isotonic calibration
- ROC-AUC: 0.80
- Sensitivity: 75%
- Specificity: 73%
- Dataset: 70,000 patient records

---

## [Unreleased]

### 🔜 Planned
- PDF report generation
- Graphical risk visualizations
- Historical tracking (with consent)
- Additional risk calculators (Framingham, SCORE)
- Medical professional dashboard
- Mobile app version
- Advanced analytics

---

[1.1.0]: https://github.com/yugayae/cvd-risk-bot/releases/tag/v1.1.0
[1.0.0]: https://github.com/yugayae/cvd-risk-bot/releases/tag/v1.0.0
