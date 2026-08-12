"""
utils/recommendation_engine.py

Generate Weather-Aware Care Recommendation (Module 4). Direct
implementation of the Phase 03 Activity Diagram "Generate Weather-Aware
Care Recommendation":

    read latest sensor reading -> read forecast
        -> both available?  no -> "Not enough data yet"
        -> yes:
            soil dry AND no rain forecast?
                yes -> "Water Today"
                no:
                    rain forecast?
                        yes -> "Skip Watering"
                        no  -> no watering action needed

IMPORTANT: the IoT Sensor Module (Module 5) hasn't been built yet, so no
route in the app currently creates a Sensor row -- `plant.sensor` is
always None right now, which means `latest_reading` passed in here will
always be None too. Per the activity diagram above, that correctly and
consistently takes the "Not enough data yet" branch. This is expected,
not a bug: Current Weather and the 5-Day Forecast (see weather_service.py)
work fully today, independent of sensor data. Nothing in this file will
need to change once Module 5 lands -- real sensor readings will simply
start flowing in and this function will start returning the Water
Today / Skip Watering / no-action branches automatically.
"""

DRY_SOIL_MOISTURE_PCT = 35.0  # below this we call the soil "dry"


def generate_recommendation(latest_reading, forecast):
    if latest_reading is None or not forecast:
        return {
            "suggestion": (
                "Not enough data yet -- a care recommendation needs both a paired sensor "
                "reading (coming in the IoT Sensor Module) and a weather forecast."
            ),
            "timeSensitive": False,
        }

    rain_soon = any(day.get("rainExpected") for day in forecast[:2])  # next 2 days
    soil_dry = latest_reading["moisture"] < DRY_SOIL_MOISTURE_PCT

    if soil_dry and not rain_soon:
        return {"suggestion": "Water Today -- soil moisture is low and no rain is expected soon.",
                "timeSensitive": True}
    if rain_soon:
        return {"suggestion": "Skip Watering -- rain is expected in the next 2 days.",
                "timeSensitive": False}
    return {"suggestion": "No watering action needed right now.", "timeSensitive": False}
