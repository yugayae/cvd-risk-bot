from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from aiogram import types
import os
from dotenv import load_dotenv

load_dotenv()

from app.schemas import PatientInput, PredictionResponse
from app.model_loader import load_model, get_model_performance_metrics
from app.shap_explainer import create_shap_explainer
from app.risk_logic import evaluate_clinical_risk

app = FastAPI(
    title="CVD Risk API",
    description="Clinical-grade cardiovascular risk assessment",
    version="1.0.0"
)

import logging
import traceback

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CORS configuration
# Parse origins with robust strip to handle potential .env whitespace
raw_origins = os.getenv("CORS_ORIGINS", "")
if not raw_origins:
    origins = ["http://localhost:3000"] # Default fallback
    logger.warning("CORS_ORIGINS not set. Defaulting to http://localhost:3000")
else:
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

logger.info(f"Active CORS Allowed Origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], # Explicitly allow methods
    allow_headers=["*"],
)

# Initialize Model and Explainer
model = load_model()
shap_explainer = create_shap_explainer(model)
model_metrics = get_model_performance_metrics()

# -------------------------
# TELEGRAM BOT INTEGRATION
# -------------------------
from app.bot_instance import bot, dp
import app.bot_setup as bot_setup  # Registers routers

WEBHOOK_PATH = "/webhook"
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")

@app.on_event("startup")
async def on_startup():
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        logging.info(f"Setting webhook to {webhook_url}")
        
        # Initialize Bot info (so Command filters work correctly)
        bot_info = await bot.get_me()
        logging.info(f"Bot initialized: @{bot_info.username}")
        
        await bot.set_webhook(
            url=webhook_url, 
            secret_token=TELEGRAM_SECRET_TOKEN,
            allowed_updates=["message", "callback_query"]
        )
    else:
        logging.warning("WEBHOOK_URL not set. Bot will not receive updates unless polling is used separately.")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Deleting webhook")
    await bot.delete_webhook()
    await bot.session.close()

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Verify Secret Token if verified
    if TELEGRAM_SECRET_TOKEN:
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if token != TELEGRAM_SECRET_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid Secret Token")

    try:
        update_data = await request.json()
        logging.info(f"Received webhook update: {update_data.get('update_id')}")
        update = types.Update(**update_data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        # Return 200 to OK Telegram even on error to prevent retry loops for bad updates
        return {"ok": False, "error":str(e)}

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
@app.get("/api/health")
def health_check():
    """Provides a basic health check endpoint."""
    return {"status": "ok", "service": "CVD Risk API", "version": "1.0.0"}

@app.get("/metrics")
@app.get("/api/metrics")
def get_metrics():
    """Returns model performance metrics."""
    return model_metrics

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/predict", response_model=PredictionResponse)
@app.post("/api/predict", response_model=PredictionResponse)
def predict_risk(patient: PatientInput):
    """
    Predicts cardiovascular risk based on patient data.
    """
    try:
        logger.info(f"Received prediction request for age {patient.age_years}")
        result = evaluate_clinical_risk(
            patient=patient,
            model=model,
            shap_explainer=shap_explainer,
            lang=patient.ui_language,
            model_metrics=model_metrics
        )
        
        result['data_validation'] = {
            'is_valid': True,
            'errors': []
        }
        
        return result
    except Exception as e:
        logger.error(f"Error during risk calculation: {str(e)}")
        logger.error(traceback.format_exc())
        from fastapi import HTTPException
        # SECURITY FIX: Do not leak exception details to the client
        raise HTTPException(status_code=500, detail="Internal Server Error: processing failed.")

from app.services.google_sheets import gs_service

@app.post("/api/log-patient-data")
async def log_patient_data(data: dict):
    """
    Logs anonymized patient data to Google Sheets after user consent.
    """
    try:
        success = await gs_service.append_patient_data(data)
        if success:
            return {"status": "success", "message": "Data logged successfully"}
        else:
            return {"status": "error", "message": "Failed to log data to Google Sheets"}
    except Exception as e:
        logger.error(f"Error logging to Google Sheets: {str(e)}")
        return {"status": "error", "message": str(e)}

# --- Static Files / Frontend ---

# Ensure absolute path for reliability
frontend_path = os.path.join(os.getcwd(), "frontend")

@app.get("/")
def read_index():
    """Serves the main frontend page."""
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not found."}

if os.path.exists(frontend_path):
    # Mount everything else from frontend folder
    # Important: Mount this AFTER all specific routes
    app.mount("/", StaticFiles(directory=frontend_path), name="static")
