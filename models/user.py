"""
models/user.py

Implements the `User` class from the Phase 03 Class Diagram.

Design note (carried over from the Phase 03 design and its accompanying
documentation): the diagram shows Gardener and NurseryOwner as subclasses of
User (generalization). For this SQLite project we implement that as a
single `users` table with a `role` column ('gardener' | 'nursery_owner')
rather than table-per-subclass inheritance -- functionally equivalent, far
less migration overhead for a student project on a one-month timeline.
Role-specific actions are guarded in the route layer (e.g. only a
nursery_owner may add a product listing), matching the Security NFR's
ownership-based access control.

Uses Flask-Login's UserMixin for session-based authentication (this
project's Security module specifies "Session Management", not JWT).
"""
import uuid
from datetime import datetime

from flask_login import UserMixin

from extensions import db


def gen_id(prefix):
    """Short, readable primary keys, e.g. 'usr_3f9a2b1c4d5e'."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    userId = db.Column("user_id", db.String, primary_key=True, default=lambda: gen_id("usr"))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True, index=True)
    passwordHash = db.Column("password_hash", db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'gardener' | 'nursery_owner'
    businessName = db.Column("business_name", db.String(160), nullable=True)  # NurseryOwner only
    createdAt = db.Column("created_at", db.DateTime, default=datetime.utcnow)

    # --- Flask-Login required interface -----------------------------------
    def get_id(self):
        # Flask-Login stores/reads this from the session cookie every request.
        return self.userId

    # --- Convenience -------------------------------------------------------
    @property
    def is_gardener(self):
        return self.role == "gardener"

    @property
    def is_nursery_owner(self):
        return self.role == "nursery_owner"

    def to_dict(self):
        return {
            "userId": self.userId,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "businessName": self.businessName,
        }

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
