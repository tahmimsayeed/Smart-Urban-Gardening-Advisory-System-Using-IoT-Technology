"""
models/sensor.py

Implements `Sensor` and `SensorReading` from the Phase 03 Class Diagram --
used starting with the IoT Sensor Module. Per the documented amendment, a
light reading was considered and explicitly dropped: SensorReading carries
only moisture, temperature, and humidity, matching the Context DFD's data
flow "Simulated Reading (Moisture, Temp, Humidity)".

One sensor pairs with exactly one plant (Plant.sensor is uselist=False).
"""
from datetime import datetime

from extensions import db
from models.user import gen_id


class Sensor(db.Model):
    __tablename__ = "sensors"

    sensorId = db.Column("sensor_id", db.String, primary_key=True, default=lambda: gen_id("sen"))
    plantId = db.Column("plant_id", db.String, db.ForeignKey("plants.plant_id"), nullable=False, unique=True)
    status = db.Column(db.String(20), default="active")  # active | inactive
    pairedAt = db.Column("paired_at", db.DateTime, default=datetime.utcnow)

    readings = db.relationship("SensorReading", backref="sensor", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {"sensorId": self.sensorId, "plantId": self.plantId, "status": self.status}


class SensorReading(db.Model):
    __tablename__ = "sensor_readings"

    readingId = db.Column("reading_id", db.String, primary_key=True, default=lambda: gen_id("rdg"))
    sensorId = db.Column("sensor_id", db.String, db.ForeignKey("sensors.sensor_id"), nullable=False)
    moisture = db.Column(db.Float, nullable=False)      # percent
    temperature = db.Column(db.Float, nullable=False)   # Celsius
    humidity = db.Column(db.Float, nullable=False)       # percent
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "readingId": self.readingId, "sensorId": self.sensorId,
            "moisture": round(self.moisture, 1), "temperature": round(self.temperature, 1),
            "humidity": round(self.humidity, 1), "timestamp": self.timestamp.isoformat(),
        }
