import os
import uuid
from datetime import date, datetime

import humanize
from app import app
from flask import flash, redirect, render_template, request, url_for, Response
from flask_login import current_user, login_required

from app.forms.exportToPDF import export_form_to_pdf
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
@app.route("/dashboard/project/<int:project_id>")
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


# Export Document to PDF
@app.route("/dashboard/project/<int:project_id>/<string:document_name>/pdf")
def export_document_pdf(project_id, document_name):
    # Query the project
    found_project = Project.query.filter_by(id=project_id).first()

    # Ensure it and the document exists
    if not found_project:
        return "Project not found", 400

    if getattr(found_project, document_name) is None:
        return "Document not found", 400

    document = getattr(found_project, document_name)

    # Export to PDF
    random_file_name = str(uuid.uuid4()) + ".pdf"
    dest_file = open(random_file_name, "w+b")
    export_status = export_form_to_pdf(document, dest_file, name=document_name)

    # Unless there is an error, return
    if export_status.err:
        return "Error exporting document to PDF", 500

    # Close the written file and read it
    dest_file.close()
    dest_file = open(random_file_name, "r+b")
    dest_file_binary = dest_file.read()

    # Close and remove the file
    dest_file.close()
    os.remove(random_file_name)

    return Response(dest_file_binary, mimetype="application/pdf", headers={"Content-Disposition": f"attachment; filename={document_name}.pdf"})
