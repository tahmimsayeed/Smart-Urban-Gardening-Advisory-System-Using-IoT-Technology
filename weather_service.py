"""
utils/weather_service.py

Current Weather + 5-Day Forecast (Module 4 sub-features). Calls
OpenWeatherMap; the 5-day forecast is cached in the WeatherForecast table
(D5 Weather Cache in the Phase 03 DFD) so a missing API key or a temporary
outage doesn't break the page -- falls back to the last cached forecast,
or a clearly-labeled placeholder if nothing has ever been cached for that
location yet. Current Weather has no cache (it's meant to be live), so it
simply reports "unavailable" rather than showing stale data.
"""
import json
from datetime import date, timedelta

import requests

from extensions import db
from models import WeatherForecast


def get_current_weather(location, api_key, current_url):
    """Returns (data_dict_or_None, source) where source is 'live' or
    'unavailable' ('no_api_key' is a special case of 'unavailable')."""
    if not api_key:
        return None, "no_api_key"

    try:
        resp = requests.get(
            current_url, params={"q": location, "appid": api_key, "units": "metric"}, timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "temperature": data["main"]["temp"],
            "feelsLike": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "windSpeed": data["wind"]["speed"],
        }, "live"
    except (requests.RequestException, KeyError, ValueError, IndexError):
        return None, "unavailable"


def get_forecast(location, api_key, base_url):
    """Returns (forecast_list, source) where source is 'live', 'cache', or
    'placeholder'. forecast_list is up to 5 dicts:
    {date, tempMin, tempMax, rainExpected}."""
    if api_key:
        try:
            resp = requests.get(
                base_url,
                params={"q": location, "appid": api_key, "units": "metric", "cnt": 40},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            forecast = _summarize_5day(data)
            _save_cache(location, forecast)
            return forecast, "live"
        except (requests.RequestException, KeyError, ValueError):
            pass  # fall through to cache

    cached = _load_cache(location)
    if cached is not None:
        return cached, "cache"

    return _placeholder_forecast(), "placeholder"


def _summarize_5day(raw_openweather_response):
    """Collapses OpenWeatherMap's 3-hourly forecast into one row per day:
    min/max temp and whether rain is expected."""
    days = {}
    for entry in raw_openweather_response.get("list", []):
        day = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]
        rain = any("rain" in w["main"].lower() for w in entry.get("weather", []))
        d = days.setdefault(day, {"date": day, "tempMin": temp, "tempMax": temp, "rainExpected": False})
        d["tempMin"] = min(d["tempMin"], temp)
        d["tempMax"] = max(d["tempMax"], temp)
        d["rainExpected"] = d["rainExpected"] or rain
    return list(days.values())[:5]


def _placeholder_forecast():
    today = date.today()
    return [
        {"date": str(today + timedelta(days=i)), "tempMin": 24.0, "tempMax": 31.0, "rainExpected": (i == 2)}
        for i in range(5)
    ]


def _save_cache(location, forecast):
    entry = WeatherForecast(location=location, forecastDate=date.today(), payload=json.dumps(forecast))
    db.session.add(entry)
    db.session.commit()


def _load_cache(location):
    entry = (
        WeatherForecast.query.filter_by(location=location)
        .order_by(WeatherForecast.fetchedAt.desc())
        .first()
    )
    return json.loads(entry.payload) if entry else None
