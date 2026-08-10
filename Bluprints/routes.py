"""
blueprints/plants/routes.py

Module 2: Plant Management (Add Plant, Edit Plant, Delete Plant, View Plant).

Follows the exact same conventions as Module 1 (blueprints/auth/routes.py):
  - @login_required for every route (session-based, via Flask-Login)
  - server-side validation via utils/validators.py, errors shown as
    Bootstrap flash messages
  - ownership-based access control (Security NFR): a Gardener may only
    view/edit/delete their OWN plants -- enforced in get_owned_plant_or_404()

Only Gardeners manage plants (Nursery Owners don't have a plant list) --
this matches the Phase 03 Use Case Diagram, where "Add New Plant" /
"View/Edit Plant Details" / "Delete Plant" are Gardener-only use cases.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import Plant
from utils.validators import validate_plant_name, validate_plant_type
from utils.access_control import require_gardener, get_owned_plant_or_404

plants_bp = Blueprint("plants", __name__, url_prefix="/plants", template_folder="../../templates/plants")


@plants_bp.route("")
@login_required
def dashboard():
    """FR: View Plant (list form) -- the Gardener's plant dashboard."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plants = Plant.query.filter_by(ownerId=current_user.userId).order_by(Plant.createdAt.desc()).all()
    return render_template("plants/dashboard.html", plants=plants)


@plants_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_plant():
    """FR: Add Plant."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        plant_type = request.form.get("type", "").strip()
        location = request.form.get("location", "").strip()

        errors = [e for e in (validate_plant_name(name), validate_plant_type(plant_type)) if e]
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("plants/add.html", name=name, type=plant_type, location=location)

        plant = Plant(ownerId=current_user.userId, name=name, type=plant_type, location=location or None)
        db.session.add(plant)
        db.session.commit()

        flash(f"'{plant.name}' was added to your garden.", "success")
        return redirect(url_for("plants.dashboard"))

    return render_template("plants/add.html")


@plants_bp.route("/<plant_id>")
@login_required
def view_plant(plant_id):
    """FR: View Plant (detail page)."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    return render_template("plants/view.html", plant=plant)


@plants_bp.route("/<plant_id>/edit", methods=["GET", "POST"])
@login_required
def edit_plant(plant_id):
    """FR: Edit Plant."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        plant_type = request.form.get("type", "").strip()
        location = request.form.get("location", "").strip()

        errors = [e for e in (validate_plant_name(name), validate_plant_type(plant_type)) if e]
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("plants/edit.html", plant=plant, name=name, type=plant_type, location=location)

        plant.name = name
        plant.type = plant_type
        plant.location = location or None
        db.session.commit()

        flash(f"'{plant.name}' was updated.", "success")
        return redirect(url_for("plants.view_plant", plant_id=plant.plantId))

    return render_template("plants/edit.html", plant=plant)


@plants_bp.route("/<plant_id>/delete", methods=["POST"])
@login_required
def delete_plant(plant_id):
    """FR: Delete Plant. POST-only and CSRF-safe-by-convention (no GET
    delete link that a crawler/prefetcher could trigger accidentally)."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    plant = get_owned_plant_or_404(plant_id)
    plant_name = plant.name
    db.session.delete(plant)
    db.session.commit()

    flash(f"'{plant_name}' and all of its sensor/diagnosis/alert history were deleted.", "info")
    return redirect(url_for("plants.dashboard"))
