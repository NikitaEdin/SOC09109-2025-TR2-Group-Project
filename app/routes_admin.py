from flask import render_template, redirect, url_for, flash
from app import app, db
from flask_login import current_user
from app.decorators import admin_required
from app.models import User, Project

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin():
        flash('You must be logged in as an admin to access this page.', 'danger')
        return redirect(url_for("login"))
    num_users = User.query.count()
    num_projects = Project.query.count()
    return render_template("admin_panel/admin_dashboard.html", num_users=num_users, num_projects=num_projects)

@app.route("/admin/users")
@admin_required
def view_users():
    if not current_user.is_authenticated or not current_user.is_admin():
        flash('You must be logged in as an admin to access this page.', 'danger')
        return redirect(url_for("login"))
    users = User.query.all()
    return render_template("admin_panel/view_users.html", users=users)

