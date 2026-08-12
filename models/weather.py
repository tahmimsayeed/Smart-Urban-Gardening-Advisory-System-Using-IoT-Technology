"""
models/weather.py

Implements `WeatherForecast` (cache) and `CareRecommendation` from the
Phase 03 Class Diagram -- used starting with the Weather Recommendation
module (Current Weather, 5-Day Forecast, Plant Care Recommendation).
"""
from datetime import date, datetime

from extensions import db
from models.user import gen_id


class WeatherForecast(db.Model):
    """Cached forecast per location, refreshed on each successful API call."""
    __tablename__ = "weather_forecasts"

    forecastId = db.Column("forecast_id", db.String, primary_key=True, default=lambda: gen_id("wth"))
    location = db.Column(db.String(120), nullable=False, index=True)
    forecastDate = db.Column("forecast_date", db.Date, default=date.today)
    payload = db.Column(db.Text, nullable=False)  # raw JSON of the 5-day forecast
    fetchedAt = db.Column("fetched_at", db.DateTime, default=datetime.utcnow)


class CareRecommendation(db.Model):
    __tablename__ = "care_recommendations"

    recommendationId = db.Column("recommendation_id", db.String, primary_key=True, default=lambda: gen_id("rec"))
    plantId = db.Column("plant_id", db.String, db.ForeignKey("plants.plant_id"), nullable=False)
    suggestionText = db.Column("suggestion_text", db.String(255), nullable=False)
    generatedDate = db.Column("generated_date", db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "recommendationId": self.recommendationId, "plantId": self.plantId,
            "suggestionText": self.suggestionText, "generatedDate": self.generatedDate.isoformat(),
        }
