# 🏥 CVD Risk Predictor - AI Telegram Bot

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**AI-powered Telegram bot for cardiovascular disease risk prediction with clinical-grade explanations**

[🤖 Try the Bot](https://t.me/cvd_risk_bot) • [📖 Documentation](#documentation) • [🚀 Deploy](#deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Deployment](#deployment)
- [Model Performance](#model-performance)
- [Contributing](#contributing)

---

## 🎯 Overview

CVD Risk Predictor is an intelligent Telegram bot that assesses cardiovascular disease risk using a calibrated CatBoost machine learning model with SHAP explanations. Available in **Russian, English, and Korean**.

### 🌟 Key Features

- 🤖 **Interactive Bot** - Easy conversational interface
- 🧠 **ML-Powered** - CatBoost model with 80% ROC-AUC
- 📊 **SHAP Explanations** - Transparent risk factors
- 🌍 **Multilingual** - ru/en/kr support
- ⚕️ **Clinical-Grade** - Confidence levels & safety warnings
- 🔒 **Privacy-First** - No data storage, rate limiting

---

## ✨ Features

### For Users
- ✅ Quick 11-question assessment
- ✅ Instant risk probability & category
- ✅ Detailed factor explanations
- ✅ Safety warnings for abnormal values
- ✅ Usage statistics

### For Developers
- ✅ FastAPI backend with async
- ✅ Docker-ready deployment
- ✅ Free hosting on Render.com
- ✅ Rate limiting (10/day per user)
- ✅ Health check monitoring

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yugayae/cvd-risk-bot.git
cd cvd-risk-bot

# 2. Install dependencies
pip install -r requirements_bot.txt

# 3. Configure
cp .env.example .env
# Add your TELEGRAM_BOT_TOKEN to .env

# 4. Run API (terminal 1)
cd cvd-risk-api
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 5. Run bot (terminal 2)
python bot/bot_main.py
```

### Deploy to Render.com (Free)

1. Push to GitHub
2. Connect to [render.com](https://render.com)
3. Create Web Service (Docker)
4. Add env var: `TELEGRAM_BOT_TOKEN`
5. Deploy! ✅

**Full guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🏗️ Architecture

```
User → Telegram Bot → FastAPI → ML Model (CatBoost + SHAP) → Results
                        ↓
                   Rate Limiter
                   Validation
                   Localization
```

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.80 |
| Sensitivity | 75% |
| Specificity | 73% |
| Dataset | 70K patients |

**Gender-specific:** Male: 0.79, Female: 0.81

---

## 📱 Usage

### Commands
- `/start` - New assessment
- `/help` - Instructions
- `/stats` - Your statistics
- `/cancel` - Cancel

### Assessment
1. Choose language
2. Answer 11 questions (age, BP, cholesterol, etc.)
3. Get detailed risk report with explanations

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **ML:** CatBoost, SHAP, scikit-learn
- **Bot:** python-telegram-bot 21.0
- **Deploy:** Docker, Render.com

---

## 📂 Project Structure

```
cvd-risk-bot/
├── bot/                    # Telegram bot
├── cvd-risk-api/          # FastAPI backend
│   └── app/               # Application logic
├── model/                 # ML model (12MB)
├── Dockerfile             # Container config
├── render.yaml            # Deployment config
└── requirements_bot.txt   # Dependencies
```

---

## ⚠️ Disclaimer

**NOT medical advice.** For informational purposes only. Consult healthcare professionals for medical decisions.

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push and open PR

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 👥 Authors

Maintained by [yugayae](https://github.com/yugayae)

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/yugayae/cvd-risk-bot/issues)
- 💬 Questions: Create an issue

---

<div align="center">

**Made with ❤️ for better healthcare**

[⬆ Back to Top](#-cvd-risk-predictor---ai-telegram-bot)

</div>
