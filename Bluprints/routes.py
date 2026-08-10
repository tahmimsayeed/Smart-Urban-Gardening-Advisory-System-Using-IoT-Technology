"""
blueprints/auth/routes.py

Module 1: Authentication (Register, Login, Logout).

Uses Flask-Login for session management (per the project's Security
requirement: "Session Management", not JWT) and Flask-Bcrypt for password
hashing. This blueprint is intentionally self-contained -- it only touches
the `User` model, so it can be tested independently of every later module.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, bcrypt
from models import User
from utils.validators import validate_name, validate_email, validate_password, validate_role

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../../templates/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Already-logged-in users don't need the register page.
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard_redirect"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "gardener")
        business_name = request.form.get("business_name", "").strip()

        # --- Input Validation (Security requirement) ------------------------
        errors = []
        for err in (validate_name(name), validate_email(email),
                    validate_password(password), validate_role(role)):
            if err:
                errors.append(err)
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if role == "nursery_owner" and not business_name:
            errors.append("Business name is required for a Nursery Owner account.")
        if not errors and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for err in errors:
                flash(err, "danger")
            # re-render with the values the user already typed, except passwords
            return render_template("auth/register.html", name=name, email=email,
                                    role=role, business_name=business_name)

        # --- Create the account ---------------------------------------------
        user = User(
            name=name,
            email=email,
            passwordHash=bcrypt.generate_password_hash(password).decode("utf-8"),
            role=role,
            businessName=business_name if role == "nursery_owner" else None,
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard_redirect"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user is None or not bcrypt.check_password_hash(user.passwordHash, password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", email=email)

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.name}!", "success")

        # Support Flask-Login's "next" redirect for @login_required pages
        next_page = request.args.get("next")
        return redirect(next_page or url_for("auth.dashboard_redirect"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/dashboard-redirect")
@login_required
def dashboard_redirect():
    """
    Sends each role to its own dashboard. Gardeners go to the Plant
    Dashboard (Module 2). Nursery Owners go to their Product Dashboard
    (Module 7, now built).
    """
    if current_user.is_gardener:
        return redirect(url_for("plants.dashboard"))
    return redirect(url_for("nursery.my_products"))
