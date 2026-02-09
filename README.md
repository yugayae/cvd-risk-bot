# 🏥 CVD Risk Predictor - AI Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**AI-powered cardiovascular disease risk prediction with clinical-grade explanations**

[🤖 Try Bot](https://t.me/cvd_risk_bot) • [📖 Русская версия](README_RU.md) • [🚀 Deploy](#deployment)

</div>

---

## 📋 Contents

- [Overview](#overview)
- [Features](#features)
- [Privacy & Data](#privacy--data-collection)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Performance](#model-performance)

---

## 🎯 Overview

Intelligent Telegram bot for cardiovascular disease risk assessment using **CatBoost ML model** with **SHAP interpretability**. Multilingual support: **Russian, English, Korean**.

### Key Features

- 🤖 Interactive Telegram bot
- 🧠 ML-powered (CatBoost, 80% ROC-AUC)
- 📊 SHAP explanations
- 🌍 3 languages (ru/en/kr)
- ⚕️ Clinical-grade output
- 🔒 Privacy-first with consent
- 📈 Auto BMI calculation
- 📊 Google Sheets logging

---

## 🔒 Privacy & Data Collection

### User Consent

- ✅ **Transparent consent** before assessment
- ✅ **Anonymous data** only (no Telegram ID, name, contacts)
- ✅ **Voluntary** - declining doesn't affect results
- ✅ **Research purpose** - improving model accuracy

### Collected (if consented)

- Medical data (age, BP, cholesterol, etc.)
- Risk results & SHAP values
- Region (e.g., "East Asia")
- Timestamp

### NOT Collected

- ❌ Telegram username/ID
- ❌ Phone/email
- ❌ Personal identifiers
- ❌ Chat history

---

## ✨ Features

### For Users

- 12-question health assessment
- Auto BMI from height/weight
- Instant risk analysis
- SHAP factor explanations
- Clinical warnings
- Quick action buttons

### For Developers

- FastAPI backend
- Docker-ready
- Free Render.com hosting
- Rate limiting (10/day)
- Health check endpoint
- Google Sheets webhook

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/yugayae/cvd-risk-bot.git
cd cvd-risk-bot

# Install
pip install -r requirements_bot.txt

# Configure
cp .env.example .env
# Add TELEGRAM_BOT_TOKEN

# Run API (terminal 1)
cd cvd-risk-api
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run bot (terminal 2)
python bot/bot_main.py
```

---

## 🌐 Deployment

### Render.com (Free)

1. Push to GitHub
2. Connect to [render.com](https://render.com)
3. New Web Service (Docker)
4. Add env var: `TELEGRAM_BOT_TOKEN`
5. Deploy!

**Optional env vars:**
- `GOOGLE_SHEETS_URL` - for data logging
- `DAILY_LIMIT=10`
- `RATE_LIMIT_MINUTES=1`

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.80 |
| Sensitivity | 75% |
| Specificity | 73% |
| Dataset | 70K patients |

**Gender-specific:** Male 0.79, Female 0.81

---

## 📱 Usage

**Commands:**
- `/start` - New assessment
- `/help` - Instructions
- `/stats` - Statistics
- `/cancel` - Cancel

**Flow:**
1. Choose language
2. Consent (optional)
3. Answer 12 health questions
4. Get detailed risk report
5. Quick actions (New/Stats/Help)

---

## 🛠️ Tech Stack

- Backend: FastAPI, Uvicorn
- ML: CatBoost, SHAP, scikit-learn
- Bot: python-telegram-bot 21.0
- Deploy: Docker, Render.com
- Logging: Google Apps Script

---

## ⚠️ Disclaimer

**NOT medical advice.** For informational purposes only.  
Consult healthcare professionals for medical decisions.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 📞 Support

- Issues: [GitHub](https://github.com/yugayae/cvd-risk-bot/issues)
- Questions: Create issue with `question` label

---

<div align="center">

**Made with ❤️ for better healthcare**

[⬆ Top](#-cvd-risk-predictor---ai-telegram-bot)

</div>
