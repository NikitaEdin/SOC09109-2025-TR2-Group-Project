from flask import render_template
from app import app, db
from app.models import User

@app.route("/admin/dashboard")
def admin_dashboard():
    num_users = User.query.count()
    num_projects = 5
    return render_template("admin_dashboard.html", num_users=num_users, num_projects=num_projects)