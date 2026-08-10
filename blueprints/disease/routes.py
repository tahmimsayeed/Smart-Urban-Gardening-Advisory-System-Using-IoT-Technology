"""
blueprints/disease/routes.py

Module 3: Disease Detection (Upload Leaf Image, Predict Disease, Confidence
Score, Treatment Recommendation, Save Disease History).

Follows the exact same conventions as Modules 1 and 2:
  - @login_required + require_gardener() (Disease Detection is a Gardener
    use case, same as Plant Management)
  - get_owned_plant_or_404() for ownership-based access control (Security
    NFR) -- a Gardener can only diagnose/view history for their OWN plants
  - server-side validation via utils/validators.py, Bootstrap flash errors

Routes are nested under /plants/<plant_id>/... , matching how Module 2
already scopes everything to a specific plant.
"""
import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required

from extensions import db
from models import DiagnosisResult
from utils.validators import validate_image_file
from utils.treatment_tips import get_treatment_tip
from utils.access_control import require_gardener, get_owned_plant_or_404
from utils.ml_predictor import predict, is_mock_mode
from utils.alert_engine import evaluate_diagnosis

disease_bp = Blueprint("disease", __name__, url_prefix="/plants", template_folder="../../templates/disease")


@disease_bp.route("/<plant_id>/diagnose", methods=["GET", "POST"])
@login_required
def diagnose(plant_id):
    """FR: Upload Leaf Image, Predict Disease, Confidence Score,
    Treatment Recommendation, Save Disease History (the "save" part)."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    mock_mode = is_mock_mode(current_app.config["ML_MODEL_PATH"], current_app.config["ML_LABELS_PATH"])

    if request.method == "POST":
        if "image" not in request.files or request.files["image"].filename == "":
            flash("Please choose a leaf image to upload.", "danger")
            return render_template("disease/diagnose.html", plant=plant, mock_mode=mock_mode)

        file = request.files["image"]
        error = validate_image_file(file.filename, current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
        if error:
            flash(error, "danger")
            return render_template("disease/diagnose.html", plant=plant, mock_mode=mock_mode)

        # --- Save the uploaded image -----------------------------------
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        ext = file.filename.rsplit(".", 1)[-1].lower()
        saved_name = f"{uuid.uuid4().hex}.{ext}"
        saved_path = os.path.join(current_app.config["UPLOAD_FOLDER"], saved_name)
        file.save(saved_path)

        # --- Predict Disease + Confidence Score --------------------------
        try:
            label, confidence, mode = predict(
                saved_path, current_app.config["ML_MODEL_PATH"], current_app.config["ML_LABELS_PATH"]
            )
        except Exception as exc:  # noqa: BLE001 -- surface any decode/inference failure to the user
            flash(f"Diagnosis failed ({exc}). Please try again with a different image.", "danger")
            return render_template("disease/diagnose.html", plant=plant, mock_mode=mock_mode)

        # --- Treatment Recommendation ------------------------------------
        treatment_tip = get_treatment_tip(label)

        # --- Save Disease History -----------------------------------------
        diagnosis = DiagnosisResult(
            plantId=plant.plantId,
            imagePath=saved_name,  # relative filename; served via the /uploads/<filename> route
            diseaseLabel=label,
            confidenceScore=confidence,
            treatmentTip=treatment_tip,
        )
        db.session.add(diagnosis)
        db.session.commit()

        # --- Trigger Disease Alert (Module 6), if warranted ------------------
        # Matches the Phase 03 Activity Diagram: a new diagnosis result is one
        # of the two events that can trigger an alert (see utils/alert_engine.py).
        evaluate_diagnosis(plant, diagnosis)

        if mode == "mock":
            flash("No trained model found yet, so this is a MOCK result for testing. "
                  "Train plant_model.keras in Colab and drop it into ml_model/ to get real predictions.",
                  "warning")

        return render_template("disease/result.html", plant=plant, diagnosis=diagnosis, mock_mode=(mode == "mock"))

    return render_template("disease/diagnose.html", plant=plant, mock_mode=mock_mode)


@disease_bp.route("/<plant_id>/history")
@login_required
def history(plant_id):
    """FR: Save Disease History (the "view" part)."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    diagnoses = (
        DiagnosisResult.query.filter_by(plantId=plant_id)
        .order_by(DiagnosisResult.timestamp.desc())
        .all()
    )
    return render_template("disease/history.html", plant=plant, diagnoses=diagnoses)
