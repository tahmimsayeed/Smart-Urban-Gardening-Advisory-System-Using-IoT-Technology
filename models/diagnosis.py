"""
models/diagnosis.py

Implements `DiagnosisResult` from the Phase 03 Class Diagram -- used
starting with the Disease Detection module.
"""
from datetime import datetime

from extensions import db
from models.user import gen_id


class DiagnosisResult(db.Model):
    __tablename__ = "diagnosis_results"

    resultId = db.Column("result_id", db.String, primary_key=True, default=lambda: gen_id("dgn"))
    plantId = db.Column("plant_id", db.String, db.ForeignKey("plants.plant_id"), nullable=False)
    imagePath = db.Column("image_path", db.String(255), nullable=False)
    diseaseLabel = db.Column("disease_label", db.String(120), nullable=False)
    confidenceScore = db.Column("confidence_score", db.Float, nullable=False)
    treatmentTip = db.Column("treatment_tip", db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def is_disease(self):
        label = self.diseaseLabel.lower()
        return "fresh" not in label and "healthy" not in label

    def to_dict(self):
        return {
            "resultId": self.resultId, "plantId": self.plantId, "diseaseLabel": self.diseaseLabel,
            "confidenceScore": round(self.confidenceScore, 3), "treatmentTip": self.treatmentTip,
            "timestamp": self.timestamp.isoformat(), "isDisease": self.is_disease(),
        }
