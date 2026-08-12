"""
utils/alert_engine.py

Trigger Threshold / Disease Alert (Module 6). Direct implementation of
the Phase 03 Activity Diagram "Trigger Threshold / Disease Alert":

    new sensor reading or diagnosis result produced
        -> threshold already configured for the plant?
            no  -> no alert evaluation performed
            yes -> compare new reading/diagnosis against saved threshold
                -> breached OR disease detected?
                    no  -> no action taken
                    yes -> create alert entry -> save with timestamp
                        -> post to Gardener's in-app notification feed

This is called from two places, matching the two events the activity
diagram reacts to -- see the small, disclosed hooks added to those files:
  - blueprints/sensors/routes.py: simulate() calls evaluate_sensor_reading()
    right after saving a new SensorReading (Module 5)
  - blueprints/disease/routes.py: diagnose() calls evaluate_diagnosis()
    right after saving a new DiagnosisResult (Module 3)
"""
from extensions import db
from models import Alert, ThresholdSetting


def evaluate_sensor_reading(plant, reading_dict):
    """reading_dict: {'moisture': ..., 'temperature': ..., 'humidity': ...}.
    Returns the created Alert, or None if no alert was warranted."""
    threshold = ThresholdSetting.query.filter_by(plantId=plant.plantId, thresholdType="moisture_min").first()
    if threshold is None:
        return None  # "threshold already configured?" -> No -> no alert evaluation performed

    if reading_dict["moisture"] < threshold.value:
        return _create_alert(
            plant.plantId, "threshold",
            f"Soil moisture ({reading_dict['moisture']:.1f}%) dropped below your "
            f"threshold of {threshold.value:.0f}% for '{plant.name}'."
        )
    return None  # breached? No -> no action taken


def evaluate_diagnosis(plant, diagnosis_result):
    """Returns the created Alert, or None if the diagnosis was healthy."""
    if not diagnosis_result.is_disease():
        return None  # disease detected? No -> no action taken

    return _create_alert(
        plant.plantId, "disease",
        f"Possible {diagnosis_result.diseaseLabel.replace('_', ' ')} detected on "
        f"'{plant.name}' (confidence {diagnosis_result.confidenceScore * 100:.0f}%)."
    )


def _create_alert(plant_id, alert_type, message):
    alert = Alert(plantId=plant_id, alertType=alert_type, message=message, status="unread")
    db.session.add(alert)
    db.session.commit()
    return alert
