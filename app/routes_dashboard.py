from datetime import date, datetime

import humanize
from app import app
from flask import flash, redirect, render_template, request, url_for, Response
from flask_login import current_user, login_required

from app.models import AuditLog, Project, User, Role

# The main/home page of the dashboard.
@app.route("/dashboard")
@login_required
def dashboard():
    # User projects
    projects = current_user.get_projects()

    # Get today's date
    today = date.today()

    # Pending projects (future dates)
    pendingProjects = Project.query.filter(Project.dateOfFlight >= today).order_by(Project.created_at.desc()).limit(3).all()

    # Past projects (past dates)
    pastProjects = Project.query.filter(Project.dateOfFlight < today).order_by(Project.created_at.desc()).limit(3).all()

    
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
    projects = Project.query.filter_by(authorID=current_user.id).order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('/dashboard/projects.html', title='projects',  use_container=False, 
                           projects=projects)

# Dashboard page for listing all projects
@app.route("/dashboard/logs")
@login_required
def logs():
    # Page number
    page = request.args.get('page', 1, type=int)  
    per_page = 10

    # User logs
    logs = AuditLog.query.filter_by(user_id=current_user.id).order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('/dashboard/logs.html', title='logs',  use_container=False, 
                           logs=logs, footer=False)

# Single project item
@app.route("/project/<int:project_id>")
@login_required
def project(project_id):
    # Query by id
    project = Project.query.get_or_404(project_id)

    # Check ownership
    if project.authorID != current_user.id:
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('dashboard'))

    # Convert datetime to human-readable format
    created_at_humanized = humanize.naturaltime(project.created_at)
    last_edited_humanized = humanize.naturaltime(project.lastEdited)

    # Determine the status (today, in x days, x days ago)
    delta = project.dateOfFlight - datetime.now().date()
    
    if delta.days == 0:
        date_status = "today"
    elif delta.days > 0:
        date_status = f"in {delta.days} day{'s' if delta.days != 1 else ''}"
    else:
        date_status = f"{abs(delta.days)} day{'s' if abs(delta.days) != 1 else ''} ago"

    return render_template('/dashboard/project.html', project=project, use_container=False, title=project.title, footer=False,
                           created_at_humanized=created_at_humanized, last_edited_humanized=last_edited_humanized,
                           date_status=date_status)
