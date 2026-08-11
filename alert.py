"""
models/alert.py

Implements `ThresholdSetting` and `Alert` from the Phase 03 Class Diagram --
used starting with the Alert Module (Threshold Alert, Disease Alert, Unread
Alert Count, Alert History).
"""
from datetime import datetime

from extensions import db
from models.user import gen_id


class ThresholdSetting(db.Model):
    __tablename__ = "threshold_settings"

    thresholdId = db.Column("threshold_id", db.String, primary_key=True, default=lambda: gen_id("thr"))
    plantId = db.Column("plant_id", db.String, db.ForeignKey("plants.plant_id"), nullable=False)
    thresholdType = db.Column("threshold_type", db.String(40), nullable=False)  # e.g. 'moisture_min'
    value = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"thresholdId": self.thresholdId, "plantId": self.plantId,
                "thresholdType": self.thresholdType, "value": self.value}


class Alert(db.Model):
    __tablename__ = "alerts"

    alertId = db.Column("alert_id", db.String, primary_key=True, default=lambda: gen_id("alt"))
    plantId = db.Column("plant_id", db.String, db.ForeignKey("plants.plant_id"), nullable=False)
    alertType = db.Column("alert_type", db.String(40), nullable=False)  # 'threshold' | 'disease'
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="unread")  # unread | acknowledged
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "alertId": self.alertId, "plantId": self.plantId, "alertType": self.alertType,
            "message": self.message, "status": self.status, "timestamp": self.timestamp.isoformat(),
        }
