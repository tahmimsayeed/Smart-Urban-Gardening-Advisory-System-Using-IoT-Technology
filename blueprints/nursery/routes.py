"""
blueprints/nursery/routes.py

Module 7: Nursery Module (Add Product, Edit Product, Delete Product,
Browse Products).

Add/Edit/Delete/View-own-listings are Nursery Owner-only use cases,
mirroring how Plant Management (Module 2) is Gardener-only. Browse
Products is a Gardener-only use case, matching FR 1.9 in the original
Requirements v2 document (the Use Case Diagram shows Gardener -> Browse
Nursery Products).

Amendment note: FR 1.16 (Edit Nursery Product Listing) and FR 1.17
(Delete Nursery Product Listing) were added to this module during this
build, beyond the original two FRs (Add Listing, Browse Products) --
documented and agreed on earlier in this conversation. No schema change
was required (see models/nursery.py); only these two new routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models import NurseryProduct
from utils.access_control import require_nursery_owner, require_gardener, get_owned_product_or_404
from utils.validators import validate_product_name, validate_product_category, parse_price, parse_quantity, \
    VALID_PRODUCT_CATEGORIES

nursery_bp = Blueprint("nursery", __name__, template_folder="../../templates/nursery")


def _validate_product_form(category, name, price_raw, quantity_raw):
    """Shared by add_product() and edit_product(). Returns (errors, price, quantity)."""
    errors = []
    for err in (validate_product_category(category), validate_product_name(name)):
        if err:
            errors.append(err)

    price, price_err = parse_price(price_raw)
    if price_err:
        errors.append(price_err)

    quantity, quantity_err = parse_quantity(quantity_raw)
    if quantity_err:
        errors.append(quantity_err)

    return errors, price, quantity


@nursery_bp.route("/nursery/products")
@login_required
def my_products():
    """Nursery Owner's own listing/inventory dashboard."""
    redirect_resp = require_nursery_owner()
    if redirect_resp:
        return redirect_resp

    products = (
        NurseryProduct.query.filter_by(nurseryOwnerId=current_user.userId)
        .order_by(NurseryProduct.createdAt.desc())
        .all()
    )
    return render_template("nursery/my_products.html", products=products)


@nursery_bp.route("/nursery/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    """FR 1.1: Add Nursery Product Listing (Tool / Plant / Fertilizer)."""
    redirect_resp = require_nursery_owner()
    if redirect_resp:
        return redirect_resp

    if request.method == "POST":
        category = request.form.get("category", "")
        name = request.form.get("name", "").strip()
        price_raw = request.form.get("price", "").strip()
        quantity_raw = request.form.get("quantity", "").strip()
        description = request.form.get("description", "").strip()

        errors, price, quantity = _validate_product_form(category, name, price_raw, quantity_raw)
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("nursery/add.html", category=category, name=name,
                                    price=price_raw, quantity=quantity_raw, description=description)

        product = NurseryProduct(
            nurseryOwnerId=current_user.userId, category=category, name=name,
            price=price, quantity=quantity, description=description or None,
        )
        db.session.add(product)
        db.session.commit()

        flash(f"'{product.name}' was added to your listings.", "success")
        return redirect(url_for("nursery.my_products"))

    return render_template("nursery/add.html")


@nursery_bp.route("/nursery/products/<product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    """FR 1.16 (amendment): Edit Nursery Product Listing."""
    redirect_resp = require_nursery_owner()
    if redirect_resp:
        return redirect_resp

    product = get_owned_product_or_404(product_id)

    if request.method == "POST":
        category = request.form.get("category", "")
        name = request.form.get("name", "").strip()
        price_raw = request.form.get("price", "").strip()
        quantity_raw = request.form.get("quantity", "").strip()
        description = request.form.get("description", "").strip()

        errors, price, quantity = _validate_product_form(category, name, price_raw, quantity_raw)
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("nursery/edit.html", product=product, category=category, name=name,
                                    price=price_raw, quantity=quantity_raw, description=description)

        product.category = category
        product.name = name
        product.price = price
        product.quantity = quantity
        product.description = description or None
        db.session.commit()

        flash(f"'{product.name}' was updated.", "success")
        return redirect(url_for("nursery.my_products"))

    return render_template("nursery/edit.html", product=product)


@nursery_bp.route("/nursery/products/<product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    """FR 1.17 (amendment): Delete Nursery Product Listing."""
    redirect_resp = require_nursery_owner()
    if redirect_resp:
        return redirect_resp

    product = get_owned_product_or_404(product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()

    flash(f"'{name}' was removed from your listings.", "info")
    return redirect(url_for("nursery.my_products"))


@nursery_bp.route("/marketplace")
@login_required
def browse():
    """FR 1.9: Browse Nursery Products (Tools, Plants & Fertilizer) --
    Gardener-facing, across every Nursery Owner's listings."""
    redirect_resp = require_gardener()
    if redirect_resp:
        return redirect_resp

    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    products_query = NurseryProduct.query
    if query:
        products_query = products_query.filter(NurseryProduct.name.ilike(f"%{query}%"))
    if category in VALID_PRODUCT_CATEGORIES:
        products_query = products_query.filter(NurseryProduct.category == category)

    products = products_query.order_by(NurseryProduct.createdAt.desc()).all()
    return render_template("nursery/browse.html", products=products, query=query, category=category)
