import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

if not BOT_TOKEN:
    raise ValueError("FATAL: BOT_TOKEN is not set in environment variables. Please check your .env file.")
