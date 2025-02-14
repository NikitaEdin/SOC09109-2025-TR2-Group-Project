from datetime import date
from app import app
from flask import render_template, request
from flask_login import current_user, login_required

from app.models import Project, User, Role

# The main/home page of the dashboard.
@app.route("/dashboard")
@login_required
def dashboard():
    # User projects
    projects = current_user.get_projects()

    # Get today's date
    today = date.today()

    # Pending projects (future dates)
    pendingProjects = Project.query.filter(Project.dateOfFlight > today).limit(3).all()

    # Past projects (past dates)
    pastProjects = Project.query.filter(Project.dateOfFlight < today).limit(3).all()

    
    return render_template('/dashboard/dashboard.html', title='dashboard', use_container=False, footer=False, 
                           projects=projects, pendingProjects=pendingProjects, pastProjects=pastProjects)

# Dashboard page for listing all projects
@app.route("/dashboard/projects")
@login_required
def projects():
    # Page number
    page = request.args.get('page', 1, type=int)  
    per_page = 10

    # User projects
    projects = Project.query.filter_by(authorID=current_user.id).paginate(page=page, per_page=per_page)
    return render_template('/dashboard/projects.html', title='projects',  use_container=False, 
                           projects=projects)

# Example page (frontend only) for a single project item.
@app.route("/dashboard/project")
@login_required
def project():
    return render_template('/dashboard/project.html')