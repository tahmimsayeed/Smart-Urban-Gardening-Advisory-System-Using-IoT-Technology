"""
utils/validators.py

Lightweight, dependency-free input validation (the project spec asks to
avoid unnecessary packages, so this skips Flask-WTF/WTForms in favor of
plain functions). Each validator returns an error string, or None if the
field is valid -- callers collect these into a list to show all problems
at once instead of one-at-a-time.
"""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_name(name):
    if not name or not name.strip():
        return "Name is required."
    if len(name.strip()) < 2:
        return "Name must be at least 2 characters."
    return None


def validate_email(email):
    if not email or not email.strip():
        return "Email is required."
    if not EMAIL_RE.match(email.strip()):
        return "Please enter a valid email address."
    return None


def validate_password(password):
    if not password:
        return "Password is required."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
        return "Password must contain both letters and numbers."
    return None


def validate_role(role):
    if role not in ("gardener", "nursery_owner"):
        return "Please select a valid account type."
    return None


def validate_image_file(filename, allowed_extensions):
    if not filename or "." not in filename:
        return "Please choose an image file."
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed_extensions:
        return f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(allowed_extensions))}."
    return None


# --- Module 2: Plant Management -------------------------------------------

def validate_plant_name(name):
    if not name or not name.strip():
        return "Plant name is required."
    if len(name.strip()) < 2:
        return "Plant name must be at least 2 characters."
    if len(name.strip()) > 120:
        return "Plant name must be under 120 characters."
    return None


def validate_plant_type(plant_type):
    if not plant_type or not plant_type.strip():
        return "Plant type is required (e.g. Tomato, Cucumber)."
    if len(plant_type.strip()) > 80:
        return "Plant type must be under 80 characters."
    return None


# --- Module 7: Nursery Module -----------------------------------------

VALID_PRODUCT_CATEGORIES = ("Tool", "Plant", "Fertilizer")


def validate_product_name(name):
    if not name or not name.strip():
        return "Product name is required."
    if len(name.strip()) < 2:
        return "Product name must be at least 2 characters."
    if len(name.strip()) > 120:
        return "Product name must be under 120 characters."
    return None


def validate_product_category(category):
    if category not in VALID_PRODUCT_CATEGORIES:
        return f"Category must be one of {', '.join(VALID_PRODUCT_CATEGORIES)}."
    return None


def parse_price(raw_price):
    """Returns (price_or_None, error_or_None)."""
    try:
        price = float(raw_price)
    except (TypeError, ValueError):
        return None, "Please enter a valid price."
    if price < 0:
        return None, "Price must be zero or greater."
    return price, None


def parse_quantity(raw_quantity):
    """Returns (quantity_or_None, error_or_None)."""
    try:
        quantity = int(raw_quantity)
    except (TypeError, ValueError):
        return None, "Please enter a valid whole number for quantity."
    if quantity < 0:
        return None, "Quantity must be zero or greater."
    return quantity, None
