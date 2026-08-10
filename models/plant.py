"""
models/plant.py

Implements the `Plant` class from the Phase 03 Class Diagram. Fields are
used starting with Module 2 (Plant Management) -- defined here now so the
schema doesn't change shape later, per the project's consistency rule.
No Garden entity: a Plant belongs directly to its owning User (Gardener).
"""
from datetime import datetime

from extensions import db
from models.user import gen_id


class Plant(db.Model):
    __tablename__ = "plants"

    plantId = db.Column("plant_id", db.String, primary_key=True, default=lambda: gen_id("plt"))
    ownerId = db.Column("owner_id", db.String, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(80), nullable=False)          # e.g. Tomato, Cucumber
    location = db.Column(db.String(120), nullable=True)      # e.g. "Balcony pot 3"
    createdAt = db.Column("created_at", db.DateTime, default=datetime.utcnow)

    owner = db.relationship("User", backref=db.backref("plants", cascade="all, delete-orphan"))
    sensor = db.relationship("Sensor", backref="plant", uselist=False, cascade="all, delete-orphan")
    diagnoses = db.relationship("DiagnosisResult", backref="plant", lazy=True, cascade="all, delete-orphan")
    thresholds = db.relationship("ThresholdSetting", backref="plant", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="plant", lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship("CareRecommendation", backref="plant", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "plantId": self.plantId, "ownerId": self.ownerId, "name": self.name,
            "type": self.type, "location": self.location,
            "hasSensor": self.sensor is not None,
        }

    def __repr__(self):
        return f"<Plant {self.name} ({self.type})>"
