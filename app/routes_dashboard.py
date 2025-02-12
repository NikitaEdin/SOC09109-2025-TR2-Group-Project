from app import app
from flask import render_template
from flask_login import current_user, login_required

from app.models import User, Role

# The main/home page of the dashboard.
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('/dashboard/dashboard.html', title='dashboard', use_container=False, footer=False)

# Dashboard page for listing all projects
@app.route("/dashboard/projects")
@login_required
def projects():
    return render_template('/dashboard/projects.html', title='projects',  use_container=False)

# Example page (frontend only) for a single project item.
@app.route("/dashboard/project")
@login_required
def project():
    return render_template('/dashboard/project.html')