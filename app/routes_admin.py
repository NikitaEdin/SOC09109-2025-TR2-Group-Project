from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import func
from app import app, db
from app.decorators import admin_required
from app.forms.editUserDetails import EditUserForm
from app.models import AuditLog, Drone, User, Role, Project

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
    return render_template("admin_panel/view_users.html", users=users, title='Users',)


@app.route("/admin/users/edit/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():  
        if form.email.data:
            user.email = form.email.data

        if form.displayname.data:
            user.displayname = form.displayname.data
        
        if form.role_id.data:
            user.role_id = form.role_id.data

        new_password = form.password.data
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for("view_users"))

    # Pre-fill form fields for the user being edited
    return render_template("admin_panel/edit_user.html", form=form, user=user, title="Edit User")


@app.route("/admin/projects")
@admin_required
def view_projects():
     # Page number
    page = request.args.get('page', 1, type=int)  
    per_page = 10

    # All projects
    projects = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template("admin_panel/view_projects.html", projects=projects, title='Projects',)


