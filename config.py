"""Application configuration for local development and Render deployment."""
import os
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-me"
    if os.environ.get("RENDER") and not os.environ.get("SECRET_KEY"):
        raise RuntimeError("Set a strong SECRET_KEY in the Render environment.")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "").lower() in {"1", "true", "yes"} or bool(os.environ.get("RENDER"))
    PERMANENT_SESSION_LIFETIME_HOURS = 12
    PERMANENT_SESSION_LIFETIME = timedelta(hours=PERMANENT_SESSION_LIFETIME_HOURS)

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "smart_garden.db"))
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    ML_MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "plant_model.keras")
    ML_LABELS_PATH = os.path.join(BASE_DIR, "ml_model", "labels.json")

    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
    OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
    DEFAULT_WEATHER_LOCATION = os.environ.get("DEFAULT_WEATHER_LOCATION", "Dhaka,BD")

    DEFAULT_MOISTURE_MIN = float(os.environ.get("DEFAULT_MOISTURE_MIN", "30"))
