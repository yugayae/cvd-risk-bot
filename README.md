# CVD Risk Assessment API 💗

An AI-powered clinical decision support system (CDSS) for cardiovascular disease risk assessment.
This project uses **CatBoost** for risk prediction and **SHAP** for explainability, wrapped in a **FastAPI** backend with a responsive **Vanilla JS** frontend and **Telegram Bot** integration.

## 🚀 Features

- **Multi-Interface**: Web Dashboard, REST API, Telegram Bot.
- **AI-Powered**: Gradient boosting model (CatBoost) with ~0.8 ROC-AUC.
- **Explainable AI**: Real-time SHAP values generation to explain individual risk factors.
- **Multi-Language**: English, Russian, Korean support.
- **Clinical Validation**: Input validation and medical safety checks.
- **Data Logging**: Optional integration with Google Sheets for data collection.

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, CatBoost, SHAP.
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Chart.js.
- **Bot**: Aiogram 3.x.
- **Tools**: Pandas, Numpy, Scikit-learn.

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/cvd-risk-api.git
    cd cvd-risk-api
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    Create a `.env` file in the root directory (see `.env.example` if available, or use the template below):
    ```env
    # Security
    BOT_TOKEN=your_telegram_bot_token
    X_INTERNAL_KEY=your_secret_key

    # CORS
    CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500

    # API
    API_BASE_URL=http://localhost:8000

    # Google Sheets (Optional)
    SPREADSHEET_ID=your_spreadsheet_id
    GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
    ```

## 🚀 Usage

### Run the Backend (API + Web)
```bash
uvicorn app.main:app --reload
```
- **Web Interface**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Run the Telegram Bot
```bash
python -m bot.main
```

## 🛡️ Security Note

This project is a **demonstrator** and a **Clinical Decision Support System (CDSS)**.
- **It does not replace professional medical advice.**
- Ensure you have appropriate user consent before logging any data.

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
