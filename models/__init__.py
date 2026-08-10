"""
models/__init__.py

Imports every model class so that:
  1. `db.create_all()` in app.py discovers all 10 tables at once (SQLAlchemy
     only registers a model with the metadata when its module is imported).
  2. Other modules can do `from models import User, Plant, ...` instead of
     reaching into individual files.

IMPORTANT: this file defines the full database schema for the whole
project up front, per the project's "maintain the same database schema
throughout" rule -- even though only `User` is exercised by Module 1
(Authentication), the rest of the schema is locked in now so later modules
don't need migrations that could conflict with earlier ones.
"""
from models.user import User
from models.plant import Plant
from models.sensor import Sensor, SensorReading
from models.diagnosis import DiagnosisResult
from models.alert import ThresholdSetting, Alert
from models.weather import WeatherForecast, CareRecommendation
from models.nursery import NurseryProduct
from models.knowledge_base import KnowledgeBaseArticle

__all__ = [
    "User", "Plant", "Sensor", "SensorReading", "DiagnosisResult",
    "ThresholdSetting", "Alert", "WeatherForecast", "CareRecommendation",
    "NurseryProduct", "KnowledgeBaseArticle",
]
