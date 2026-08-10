"""
utils/access_control.py

Shared ownership-based access control helpers (Security NFR). Originally
defined as private functions inside blueprints/plants/routes.py (Module 2);
moved here, unchanged in behavior, so Module 3 (Disease Detection) and
later plant-scoped modules (IoT Sensor, Alert, Weather) can reuse the exact
same rule instead of importing another blueprint's underscore-prefixed
helpers or re-implementing the logic slightly differently each time.

This is a pure relocation, not a behavior change -- see git-style diff in
the project notes if you want to confirm both functions are byte-for-byte
identical to the Module 2 originals.
"""
from flask import redirect, url_for, flash, abort
from flask_login import current_user

from models import Plant, NurseryProduct


def require_gardener():
    """Returns a redirect response if the current user is NOT a Gardener,
    or None if they are -- callers do `resp = require_gardener(); if resp:
    return resp`. Used by any module whose use cases are Gardener-only
    (Plant Management, Disease Detection, ...)."""
    if not current_user.is_gardener:
        flash("This feature is only available for Gardener accounts.", "warning")
        return redirect(url_for("auth.dashboard_redirect"))
    return None


def get_owned_plant_or_404(plant_id):
    """Returns the plant only if it belongs to the current user, otherwise
    404s -- deliberately NOT a 403, so a user probing other plant IDs can't
    even tell whether a given ID exists."""
    plant = Plant.query.get(plant_id)
    if plant is None or plant.ownerId != current_user.userId:
        abort(404)
    return plant


def require_nursery_owner():
    """Same pattern as require_gardener(), for the Nursery Module (Module
    7): Add/Edit/Delete/View-own-listings are Nursery Owner-only use
    cases."""
    if not current_user.is_nursery_owner:
        flash("This feature is only available for Nursery Owner accounts.", "warning")
        return redirect(url_for("auth.dashboard_redirect"))
    return None


def get_owned_product_or_404(product_id):
    """Same pattern as get_owned_plant_or_404(): returns the product only
    if it belongs to the current user, otherwise 404s."""
    product = NurseryProduct.query.get(product_id)
    if product is None or product.nurseryOwnerId != current_user.userId:
        abort(404)
    return product
