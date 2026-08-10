"""
models/nursery.py

Implements `NurseryProduct` from the Phase 03 Class Diagram -- used
starting with the Nursery Module.

Amendment note: FR 1.16 (Edit Nursery Product Listing) and FR 1.17 (Delete
Nursery Product Listing) were added to Process 7.0 Manage Nursery
Marketplace during this build (beyond the original 15 FRs in Requirements
v2, which only had Add Listing + Browse). No schema change was required
for that amendment -- Edit/Delete operate on the same table below; only
new routes are needed when the Nursery Module is built.
"""
from datetime import datetime

from extensions import db
from models.user import gen_id

VALID_CATEGORIES = ("Tool", "Plant", "Fertilizer")


class NurseryProduct(db.Model):
    __tablename__ = "nursery_products"

    productId = db.Column("product_id", db.String, primary_key=True, default=lambda: gen_id("prd"))
    nurseryOwnerId = db.Column("nursery_owner_id", db.String, db.ForeignKey("users.user_id"), nullable=False)
    category = db.Column(db.String(20), nullable=False)  # Tool | Plant | Fertilizer
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    createdAt = db.Column("created_at", db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column("updated_at", db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship("User", backref=db.backref("products", cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            "productId": self.productId, "nurseryOwnerId": self.nurseryOwnerId,
            "category": self.category, "name": self.name, "price": self.price,
            "quantity": self.quantity, "description": self.description,
        }

    def __repr__(self):
        return f"<NurseryProduct {self.name} ({self.category})>"
