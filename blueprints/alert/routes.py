"""
blueprints/alerts/routes.py

Module 6: Alert Module (Threshold Alert, Disease Alert, Unread Alert
Count, Alert History).

Set Threshold Alert Values is a direct user action (this blueprint).
Trigger Threshold / Disease Alert happens automatically via
utils/alert_engine.py, called from Module 5's simulate() and Module 3's
diagnose() routes -- see the small, disclosed hooks added to those two
files. Unread Alert Count is exposed globally via a context processor in
app.py so it can show as a navbar badge on every page.

Note this blueprint does NOT use a single url_prefix, since it needs both
plant-scoped routes (/plants/<id>/...) and a global route (/alerts) --
each route below specifies its own full path instead.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Plant, ThresholdSetting, Alert
from utils.access_control import require_gardener, get_owned_plant_or_404

alerts_bp = Blueprint("alerts", __name__, template_folder="../../templates/alerts")


@alerts_bp.route("/plants/<plant_id>/thresholds", methods=["GET", "POST"])
@login_required
def thresholds(plant_id):
    """FR: Set Threshold Alert Values."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    threshold = ThresholdSetting.query.filter_by(plantId=plant_id, thresholdType="moisture_min").first()

    if request.method == "POST":
        raw_value = request.form.get("moisture_min", "").strip()
        try:
            value = float(raw_value)
        except ValueError:
            flash("Please enter a valid number for the moisture threshold.", "danger")
            return render_template("alerts/thresholds.html", plant=plant, threshold=threshold)

        if value < 0 or value > 100:
            flash("Moisture threshold must be between 0 and 100.", "danger")
            return render_template("alerts/thresholds.html", plant=plant, threshold=threshold)

        if threshold is None:
            threshold = ThresholdSetting(plantId=plant_id, thresholdType="moisture_min", value=value)
            db.session.add(threshold)
        else:
            threshold.value = value
        db.session.commit()

        flash(f"Alert threshold saved -- you'll be notified if soil moisture drops below {value:.0f}%.", "success")
        return redirect(url_for("plants.view_plant", plant_id=plant_id))

    return render_template("alerts/thresholds.html", plant=plant, threshold=threshold)


@alerts_bp.route("/plants/<plant_id>/alerts")
@login_required
def plant_alerts(plant_id):
    """FR: Alert History, scoped to one plant."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    plant_alert_list = Alert.query.filter_by(plantId=plant_id).order_by(Alert.timestamp.desc()).all()
    return render_template("alerts/plant_alerts.html", plant=plant, alerts=plant_alert_list)


@alerts_bp.route("/plants/<plant_id>/alerts/<alert_id>/acknowledge", methods=["POST"])
@login_required
def acknowledge(plant_id, alert_id):
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    alert = Alert.query.get(alert_id)
    if alert is None or alert.plantId != plant.plantId:
        flash("Alert not found.", "danger")
        return redirect(url_for("alerts.plant_alerts", plant_id=plant_id))

    alert.status = "acknowledged"
    db.session.commit()
    return redirect(request.referrer or url_for("alerts.plant_alerts", plant_id=plant_id))


@alerts_bp.route("/alerts")
@login_required
def all_alerts():
    """FR: Alert History + Unread Alert Count, across every plant the
    Gardener owns -- the global notification feed."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    my_plants = Plant.query.filter_by(ownerId=current_user.userId).all()
    plant_ids = [p.plantId for p in my_plants]
    plants_by_id = {p.plantId: p for p in my_plants}

    feed = []
    if plant_ids:
        feed = (
            Alert.query.filter(Alert.plantId.in_(plant_ids))
            .order_by(Alert.timestamp.desc())
            .limit(50)
            .all()
        )
    return render_template("alerts/all_alerts.html", feed=feed, plants_by_id=plants_by_id)


@alerts_bp.route("/alerts/<alert_id>/acknowledge", methods=["POST"])
@login_required
def acknowledge_global(alert_id):
    alert = Alert.query.get(alert_id)
    plant = Plant.query.get(alert.plantId) if alert else None
    if plant is None or plant.ownerId != current_user.userId:
        flash("Alert not found.", "danger")
        return redirect(url_for("alerts.all_alerts"))

    alert.status = "acknowledged"
    db.session.commit()
    return redirect(url_for("alerts.all_alerts"))
