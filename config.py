import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("GONKA_BROKER_API_KEY", "").strip()
    BASE_URL = (os.getenv("GONKA_BROKER_URL") or "").strip().rstrip("/")
    MODEL = os.getenv("GONKA_MODEL", "").strip()
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    def validate(self):
        if not self.API_KEY or not self.BASE_URL:
            raise RuntimeError("Missing configuration in .env: GONKA_BROKER_URL or GONKA_BROKER_API_KEY.")
        if not self.MODEL:
            raise RuntimeError("Missing configuration in .env: GONKA_MODEL.")
