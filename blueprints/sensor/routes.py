"""
blueprints/sensors/routes.py

Module 5: IoT Sensor Module (Register and Pair IoT Sensor Node, Simulated
Temperature, Simulated Humidity, Simulated Soil Moisture).

Documented amendment: a "Simulated Light" reading was considered during
this build and explicitly dropped -- see utils/sensor_simulator.py. Only
moisture, temperature, and humidity are simulated, matching the
Sensor/SensorReading models already defined in models/sensor.py since
Module 1's foundational schema.

Follows the exact same conventions as Modules 1-4:
  - @login_required + require_gardener()
  - get_owned_plant_or_404() for ownership-based access control

Building this module also "unlocks" Module 4's Care Recommendation: once
a sensor is paired here and has at least one simulated reading,
utils/recommendation_engine.py (unchanged) automatically starts returning
real Water Today / Skip Watering advice instead of "Not enough data yet."
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from extensions import db
from models import Sensor, SensorReading
from utils.access_control import require_gardener, get_owned_plant_or_404
from utils.sensor_simulator import simulate_reading
from utils.alert_engine import evaluate_sensor_reading

sensors_bp = Blueprint("sensors", __name__, url_prefix="/plants", template_folder="../../templates/sensors")


@sensors_bp.route("/<plant_id>/sensor")
@login_required
def sensor(plant_id):
    """Sensor status + reading history for one plant."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    readings = []
    if plant.sensor is not None:
        readings = (
            SensorReading.query.filter_by(sensorId=plant.sensor.sensorId)
            .order_by(SensorReading.timestamp.desc())
            .limit(20)
            .all()
        )
    return render_template("sensors/sensor.html", plant=plant, readings=readings)


@sensors_bp.route("/<plant_id>/sensor/pair", methods=["POST"])
@login_required
def pair_sensor(plant_id):
    """FR: Register and Pair IoT Sensor Node -- 1 sensor per plant."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    if plant.sensor is not None:
        flash("This plant already has a sensor paired.", "warning")
        return redirect(url_for("sensors.sensor", plant_id=plant_id))

    new_sensor = Sensor(plantId=plant.plantId, status="active")
    db.session.add(new_sensor)
    db.session.commit()

    flash(f"A sensor has been registered and paired to '{plant.name}'.", "success")
    return redirect(url_for("sensors.sensor", plant_id=plant_id))


@sensors_bp.route("/<plant_id>/sensor/simulate", methods=["POST"])
@login_required
def simulate(plant_id):
    """FR: Simulated Temperature, Simulated Humidity, Simulated Soil Moisture."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    if plant.sensor is None:
        flash("Pair a sensor to this plant first.", "danger")
        return redirect(url_for("sensors.sensor", plant_id=plant_id))

    values = simulate_reading(plant.sensor.sensorId)
    reading = SensorReading(sensorId=plant.sensor.sensorId, **values)
    db.session.add(reading)
    db.session.commit()

    # --- Trigger Threshold Alert (Module 6), if warranted ----------------
    # Matches the Phase 03 Activity Diagram: a new sensor reading is one of
    # the two events that can trigger an alert (see utils/alert_engine.py).
    evaluate_sensor_reading(plant, values)

    flash("New sensor reading recorded.", "success")
    return redirect(url_for("sensors.sensor", plant_id=plant_id))
