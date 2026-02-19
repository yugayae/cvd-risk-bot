import httpx
from bot.config import API_BASE_URL

async def get_risk_prediction(data: dict) -> dict:
    """
    Sends patient data to the backend API and returns the prediction.
    """
    url = f"{API_BASE_URL}/predict"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"API Request Failed: {e}")
            return {"error": str(e)}
