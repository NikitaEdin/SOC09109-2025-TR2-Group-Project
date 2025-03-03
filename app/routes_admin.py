from flask import render_template, redirect, url_for, flash
from sqlalchemy import func
from app import app, db
from app.decorators import admin_required
from app.models import AuditLog, Drone, User, Project

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    
    num_users = User.query.count()
    num_projects = Project.query.count()
    num_logs = AuditLog.query.count()
    num_drones = Drone.query.count()


    # Projects by type
    projects_by_type = dict(db.session.query(Project.projectType, func.count(Project.id)).group_by(Project.projectType).all())

    # Recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()

    return render_template(
        "admin_panel/admin_dashboard.html",
        num_users=num_users,
        num_projects=num_projects,
        num_logs=num_logs,
        projects_by_type=projects_by_type,
        recent_projects=recent_projects,
        num_drones=num_drones,
       
        title='admin panel',
        use_container=False
    )

@app.route("/admin/users")
@admin_required
def view_users():
    users = User.query.all()
    return render_template("admin_panel/view_users.html", users=users,
                            title='users',)

