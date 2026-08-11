"""
utils/sensor_simulator.py

Simulated Temperature, Simulated Humidity, Simulated Soil Moisture
(Module 5). Per the Phase 02 Requirements, this project is explicitly
scoped to simulated sensor data (no real IoT hardware) -- this module
stands in for the "SENSOR NODE (SIMULATED)" external entity in the
Context DFD.

Per the documented amendment made during this build (light sensor was
considered and explicitly dropped), a reading only ever contains
moisture, temperature, and humidity -- matching the SensorReading model
already defined in models/sensor.py since Module 1's foundational schema
and the Context DFD's data flow "Simulated Reading (Moisture, Temp,
Humidity)".

Each call produces one plausible reading, drifting a little from the
sensor's previous value (kept in memory only, per Flask process) instead
of pure random noise -- so repeated simulated readings look like a real
pot slowly drying out rather than jumping around unrealistically.
"""
import random

# sensor_id -> {"moisture": ..., "temperature": ..., "humidity": ...}
# In-memory only: resets when the Flask process restarts. That's fine for
# a simulated-data MVP -- the *saved* readings persist in the database
# regardless, this cache just makes consecutive simulated values trend
# realistically within one run of the app.
_last_values = {}


def simulate_reading(sensor_id):
    prev = _last_values.get(sensor_id, {
        "moisture": random.uniform(40, 70),
        "temperature": random.uniform(22, 30),
        "humidity": random.uniform(50, 70),
    })

    moisture = _drift(prev["moisture"], step=3.0, lo=5, hi=95)
    temperature = _drift(prev["temperature"], step=0.8, lo=10, hi=42)
    humidity = _drift(prev["humidity"], step=2.5, lo=15, hi=95)

    _last_values[sensor_id] = {"moisture": moisture, "temperature": temperature, "humidity": humidity}
    return {"moisture": moisture, "temperature": temperature, "humidity": humidity}


def _drift(value, step, lo, hi):
    # Slight downward bias on the random walk -- mimics a pot drying out
    # over time rather than random noise with no direction.
    delta = random.uniform(-step, step * 0.6)
    return max(lo, min(hi, value + delta))
