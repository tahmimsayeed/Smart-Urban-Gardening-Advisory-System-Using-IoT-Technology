"""
blueprints/weather/routes.py

Module 4: Weather Recommendation (Current Weather, 5-Day Forecast, Plant
Care Recommendation).

Follows the exact same conventions as Modules 1-3:
  - @login_required + require_gardener() (Weather Recommendation is a
    Gardener use case, same as Plant Management and Disease Detection)
  - get_owned_plant_or_404() for ownership-based access control
"""
from flask import Blueprint, render_template, request, current_app
from flask_login import login_required

from extensions import db
from models import CareRecommendation, SensorReading
from utils.access_control import require_gardener, get_owned_plant_or_404
from utils.weather_service import get_current_weather, get_forecast
from utils.recommendation_engine import generate_recommendation

weather_bp = Blueprint("weather", __name__, url_prefix="/plants", template_folder="../../templates/weather")


@weather_bp.route("/<plant_id>/weather")
@login_required
def weather(plant_id):
    """FR: Current Weather, 5-Day Forecast, Plant Care Recommendation."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    location = request.args.get("location", "").strip() or current_app.config["DEFAULT_WEATHER_LOCATION"]

    # --- Current Weather -----------------------------------------------
    current, current_source = get_current_weather(
        location, current_app.config["OPENWEATHER_API_KEY"], current_app.config["OPENWEATHER_CURRENT_URL"]
    )

    # --- 5-Day Forecast --------------------------------------------------
    forecast, forecast_source = get_forecast(
        location, current_app.config["OPENWEATHER_API_KEY"], current_app.config["OPENWEATHER_BASE_URL"]
    )

    # --- Plant Care Recommendation ----------------------------------------
    # plant.sensor is None until the IoT Sensor Module (Module 5) exists --
    # see the note in utils/recommendation_engine.py.
    latest_reading = None
    if plant.sensor is not None:
        reading = (
            SensorReading.query.filter_by(sensorId=plant.sensor.sensorId)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )
        if reading is not None:
            latest_reading = {
                "moisture": reading.moisture,
                "temperature": reading.temperature,
                "humidity": reading.humidity,
            }

    result = generate_recommendation(latest_reading, forecast)

    # Avoid inserting a duplicate row on every page refresh when nothing
    # about the recommendation has actually changed.
    last = (
        CareRecommendation.query.filter_by(plantId=plant.plantId)
        .order_by(CareRecommendation.generatedDate.desc())
        .first()
    )
    if last is None or last.suggestionText != result["suggestion"]:
        recommendation = CareRecommendation(plantId=plant.plantId, suggestionText=result["suggestion"])
        db.session.add(recommendation)
        db.session.commit()
    else:
        recommendation = last

    return render_template(
        "weather/weather.html",
        plant=plant,
        location=location,
        current=current,
        current_source=current_source,
        forecast=forecast,
        forecast_source=forecast_source,
        recommendation=recommendation,
        time_sensitive=result["timeSensitive"],
        has_sensor=(plant.sensor is not None),
    )
