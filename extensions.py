"""
extensions.py

Single shared instances of Flask extensions. Every blueprint/model imports
from here instead of creating its own instance, which avoids circular
imports between app.py, models/, and blueprints/.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Where Flask-Login redirects an anonymous user who hits a @login_required route
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
