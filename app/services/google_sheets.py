import os
import logging
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.spreadsheet_id = os.getenv("SPREADSHEET_ID")
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials.json")
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self._service = None

    def _get_service(self):
        if self._service is None:
            if not os.path.exists(self.credentials_path):
                logger.warning(f"Google Sheets credentials file not found: {self.credentials_path}. Data logging will be disabled.")
                return None
            
            try:
                creds = service_account.Credentials.from_service_account_file(
                    self.credentials_path, scopes=self.scopes)
                self._service = build('sheets', 'v4', credentials=creds)
            except Exception as e:
                logger.error(f"Failed to initialize Google Sheets service: {e}")
                return None
        return self._service

    async def append_patient_data(self, data: dict):
        """
        Appends anonymized patient data to the Google Sheet.
        """
        service = self._get_service()
        if not service or not self.spreadsheet_id:
            return False

        try:
            # Prepare row data according to user request:
            # 1.data, 2.region, 3.age, 4.sex, 5.systolic_bp, 6.diastolic_bp, 7.cholesterol_cat, 
            # 8.glucose_cat, 9.bmi, 10.smoking, 11.alcohol, 12.physical_activity, 
            # 13.risk_probability, 14.risk_category
            
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # 1. data
                data.get("region", "unknown"),                # 2. region
                data.get("age_years"),                        # 3. age
                "Male" if data.get("gender") == 2 else "Female", # 4. sex
                data.get("ap_hi"),                            # 5. systolic_bp
                data.get("ap_lo"),                            # 6. diastolic_bp
                data.get("cholesterol"),                      # 7. cholesterol_cat
                data.get("gluc"),                             # 8. glucose_cat
                data.get("bmi"),                              # 9. bmi
                "Yes" if data.get("smoke") else "No",         # 10. smoking
                "Yes" if data.get("alco") else "No",          # 11. alcohol
                "Yes" if data.get("active") else "No",         # 12. physical_activity
                f"{data.get('risk_probability')}%",           # 13. risk_probability
                data.get("risk_category")                     # 14. risk_category
            ]

            values = [row]
            body = {'values': values}
            
            # Assuming 'Sheet1!A1' as range, appending to the end
            result = service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body=body
            ).execute()
            
            logger.info(f"Successfully appended data to Google Sheets: {result.get('updates').get('updatedRange')}")
            return True
        except HttpError as error:
            logger.error(f"Google Sheets API Error: {error}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during GSheets logging: {e}")
            return False

# Global instance
gs_service = GoogleSheetsService()
