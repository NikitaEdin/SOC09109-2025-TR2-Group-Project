import re
from wtforms import ValidationError

def validate_password(form, field):
    """Enforces minimal password strength: at least 4 characters, 1 letter, 1 digit."""
    password = field.data

    if not password:
        return  # Empty password for  Optional()

    if len(password) < 4:
        raise ValidationError("Password must be at least 4 characters long.")

    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must contain at least one letter.")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number.")
