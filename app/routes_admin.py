from flask import render_template, redirect, url_for, flash
from app import app, db
from flask_login import current_user
from app.models import User

@app.route("/admin/dashboard")
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin():
        flash('You must be logged in as an admin to access this page.', 'danger')
        return redirect(url_for("login"))
    num_users = User.query.count()
    num_projects = 5
    return render_template("admin_panel/admin_dashboard.html", num_users=num_users, num_projects=num_projects)

@app.route("/admin/users")
def view_users():
    if not current_user.is_authenticated or not current_user.is_admin():
        flash('You must be logged in as an admin to access this page.', 'danger')
        return redirect(url_for("login"))
    users = User.query.all()
    return render_template("admin_panel/view_users.html", users=users)

