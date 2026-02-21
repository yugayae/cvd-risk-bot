import os
import logging
import httpx

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.webhook_url = os.getenv("GOOGLE_SHEETS_URL")

    async def append_patient_data(self, data: dict):
        """
        Appends anonymized patient data to the Google Sheet via Apps Script Web App.
        """
        if not self.webhook_url:
            logger.warning("GOOGLE_SHEETS_URL is not set. Data logging is disabled.")
            return False

        try:
            # Map input data (frontend & bot) to expected Apps Script schema
            payload = {
                "region": data.get("region", "unknown"),
                "age": data.get("age_years", ""),
                "sex": "Male" if data.get("gender") == 2 else "Female",
                "systolic_bp": data.get("ap_hi", ""),
                "diastolic_bp": data.get("ap_lo", ""),
                "cholesterol_cat": data.get("cholesterol", ""),
                "glucose_cat": data.get("gluc", ""),
                "bmi": data.get("bmi", ""),
                "smoking": "Yes" if data.get("smoke") else "No",
                "alcohol": "Yes" if data.get("alco") else "No",
                "physical_activity": "Yes" if data.get("active") else "No",
                "risk_probability": f"{data.get('risk_probability', '')}%",
                "risk_category": data.get("risk_category", "")
            }

            async with httpx.AsyncClient() as client:
                # App Script requires follow_redirects=True for POST requests
                response = await client.post(
                    self.webhook_url, 
                    json=payload,
                    follow_redirects=True,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "ok":
                        logger.info("Successfully appended data to Google Sheets via Web App.")
                        return True
                    else:
                        logger.error(f"Google Sheets Web App error: {result.get('message')}")
                        return False
                else:
                    logger.error(f"Failed to post to Google Sheets Web App. Status: {response.status_code}")
                    return False
                
        except Exception as e:
            logger.error(f"Unexpected error during GSheets logging: {e}")
            return False

# Global instance
gs_service = GoogleSheetsService()
