import httpx
from bot.config import API_BASE_URL
from app.core.state import global_state
from app.risk_logic import evaluate_clinical_risk
from app.schemas import PatientInput

async def get_risk_prediction(data: dict) -> dict:
    """
    Sends patient data to the backend API or uses internal logic if available.
    """
    # Try internal logic first (Fast path, no HTTP overhead/errors)
    if global_state.model is not None:
        try:
            # Convert dict to PatientInput schema
            patient_input = PatientInput(**data)
            
            # Execute logic directly
            result = evaluate_clinical_risk(
                patient=patient_input,
                model=global_state.model,
                shap_explainer=global_state.shap_explainer,
                lang=data.get("ui_language", "en")
            )
            # Return as dict (compatible with API response structure)
            return result.model_dump()
        except Exception as e:
            print(f"Internal Prediction Error: {e}")
            return {"error": str(e)}

    # Fallback to HTTP API (if running standalone)
    url = f"{API_BASE_URL}/predict"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"API Request Failed: {e}")
            return {"error": str(e)}
