from functools import wraps
from flask import abort
from flask_login import current_user

# Custom decorator for authenticated and admin locked access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            # If the user is not authenticated or is not an admin, raise 403
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
