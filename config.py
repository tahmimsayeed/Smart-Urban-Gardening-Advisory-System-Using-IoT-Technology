"""
config.py

Central configuration for the Smart Urban Gardening Advisory System.
All secrets/paths are overridable via environment variables so the same
code works in development and on a grader's machine without edits.
"""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))  # loads OPENWEATHER_API_KEY etc. from .env if present


class Config:
    # --- Flask / session security ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME_HOURS = 12

    # --- Database (SQLite + SQLAlchemy ORM, per project spec) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'smart_garden.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- File uploads (leaf images for Disease Detection module) ---
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB

    # --- ML model (Disease Detection module, loaded at startup) ---
    ML_MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "plant_model.keras")
    ML_LABELS_PATH = os.path.join(BASE_DIR, "ml_model", "labels.json")

    # --- OpenWeatherMap API (Weather Recommendation module) ---
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
    OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
    # Plant.location is free text (e.g. "Balcony pot 1, south-facing"), not
    # a geocodable place -- Weather Recommendation uses this default city
    # unless the Gardener overrides it on the weather page.
    DEFAULT_WEATHER_LOCATION = os.environ.get("DEFAULT_WEATHER_LOCATION", "Dhaka,BD")

    # --- Alert Module defaults ---
    DEFAULT_MOISTURE_MIN = float(os.environ.get("DEFAULT_MOISTURE_MIN", "30"))
