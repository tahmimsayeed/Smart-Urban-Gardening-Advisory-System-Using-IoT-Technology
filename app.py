"""
app.py

Application factory for the Smart Urban Gardening Advisory System.

Run directly for development:
    python app.py
"""
from flask import Flask

from config import Config
from extensions import db, bcrypt, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Initialize extensions ---------------------------------------------
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # --- Flask-Login: how to load a user from the session cookie ------------
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # --- Register blueprints -------------------------------------------------
    # Each module registers its own blueprint here, one line each, without
    # touching this file's other lines -- keeps merge conflicts and
    # accidental breakage low.
    from blueprints.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from blueprints.plants.routes import plants_bp
    app.register_blueprint(plants_bp)

    from blueprints.disease.routes import disease_bp
    app.register_blueprint(disease_bp)

    from blueprints.weather.routes import weather_bp
    app.register_blueprint(weather_bp)

    from blueprints.sensors.routes import sensors_bp
    app.register_blueprint(sensors_bp)

    from blueprints.alerts.routes import alerts_bp
    app.register_blueprint(alerts_bp)

    from blueprints.nursery.routes import nursery_bp
    app.register_blueprint(nursery_bp)

    from blueprints.knowledge_base.routes import knowledge_base_bp
    app.register_blueprint(knowledge_base_bp)

    # --- Create database tables (all 10, per models/__init__.py) ------------
    with app.app_context():
        db.create_all()

        # Module 8: Knowledge Base -- seed once, automatically, if the
        # table is empty. Safe to run on every startup: seed_if_empty()
        # is a no-op after the first successful run.
        from utils.seed_knowledge_base import seed_if_empty
        seed_if_empty()

    # --- Friendly root route: send visitors straight to login ---------------
    @app.route("/")
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for("auth.dashboard_redirect"))
        return redirect(url_for("auth.login"))

    # --- Serve uploaded leaf images (Module 3: Disease Detection) -----------
    # Login-protected since these are photos of a specific user's plants,
    # not public assets -- kept separate from static/ (which Flask serves
    # unauthenticated) for that reason.
    from flask_login import login_required

    @app.route("/uploads/<path:filename>")
    @login_required
    def uploaded_file(filename):
        from flask import send_from_directory
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.errorhandler(404)
    def not_found(e):
        return "Page not found.", 404

    # --- Unread Alert Count for the navbar badge (Module 6) -----------------
    # A context processor makes `unread_alert_count` available in every
    # template automatically, without each route having to pass it in.
    @app.context_processor
    def inject_unread_alert_count():
        from flask_login import current_user
        from models import Alert, Plant

        if not current_user.is_authenticated or not current_user.is_gardener:
            return {"unread_alert_count": 0}

        plant_ids = [p.plantId for p in Plant.query.filter_by(ownerId=current_user.userId).all()]
        if not plant_ids:
            return {"unread_alert_count": 0}

        count = Alert.query.filter(Alert.plantId.in_(plant_ids), Alert.status == "unread").count()
        return {"unread_alert_count": count}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
