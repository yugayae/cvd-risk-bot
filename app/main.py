from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# --- Prediction Logic & Endpoints ---

@app.get("/health")
@app.get("/api/health")
def health_check():
    """Provides a basic health check endpoint."""
    return {"status": "ok"}

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
