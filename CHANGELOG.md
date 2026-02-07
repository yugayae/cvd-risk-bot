# Changelog

All notable changes to CVD Risk Predictor will be documented here.

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
- Quick action buttons after results
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
- Additional risk calculators
- Mobile app version
- Medical professional dashboard

---

## Version Format

[MAJOR.MINOR.PATCH]
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

---

[1.0.0]: https://github.com/yugayae/cvd-risk-bot/releases/tag/v1.0.0
