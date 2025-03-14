from copy import deepcopy
from datetime import datetime, timezone
from app import app, db
from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.AuditLogger import AuditLogger
from app.forms.createProject import EditProject, ProjectLocation, ProjectType, ProjectDetails
from app.models import Project

from app.forms.jsons.viabilityStudyTemplate import ViabilityStudyTemplate
from app.forms.jsons.siteEvaluationTemplate import SiteEvaluationTemplate

# Step 1: Get location of the project
@app.route("/create_project/location", methods=['GET','POST'])
@login_required
def new_project_location():
    form = ProjectLocation()
    
    # Reset session values
    session.pop('longitude', None)
    session.pop('latitude', None)
    session.pop('projectType', None)

    # Default Map location - Merchiston Campus
    default_latitude = 55.932850
    default_longitude = -3.213431
    default_zoom = 15

    # on form submit
    if form.validate_on_submit():
        session['longitude'] = form.longitude.data
        session['latitude'] = form.latitude.data
        return redirect(url_for('new_project_type'))
    
    
    return render_template('/create_project/new_project_location.html', form=form, footer=False, title='Where?',
                           default_latitude=default_latitude, default_longitude=default_longitude, default_zoom=default_zoom)

# Step 2: Get project type
@app.route("/create_project/type", methods=['GET','POST'])
@login_required
def new_project_type():
    form = ProjectType()

    # Was step 1 skipped?
    if not session.get('longitude') and not session.get('latitude'):
        flash('You must specify project location first.', 'danger')
        return redirect(url_for('new_project_location'))

    # on form submit
    if form.validate_on_submit():
        session['projectType'] = form.projectType.data
        return redirect(url_for('new_project_details'))

    return render_template('/create_project/new_project_type.html', form=form, footer=False, title='What type?')

# Step 3: Get the required project details
@app.route("/create_project/details", methods=['GET','POST'])
@login_required
def new_project_details():
    form = ProjectDetails()

    if not session.get('longitude') and not session.get('latitude') and not session.get('projectType'):
        flash('Project creation steps were not completed correctly.', 'danger')
        return redirect(url_for('new_project_location'))

    if form.validate_on_submit():
        # Retrieve session data
        longitude = session.get('longitude')
        latitude = session.get('latitude')
        project_type = session.get('projectType')

        # Get dataOfFlight to correct format

        # prepopulate form
        users_name = current_user.username

        if current_user.displayname:
            users_name = current_user.displayname

        flight_code = Project.get_new_flightCode(form.projectPurposeID.data)

        viability_study_value = deepcopy(ViabilityStudyTemplate)

        for template in viability_study_value:
            for section in template['form']['sections']:
                for field in section['fields']:
                    if field['id'] == 'flightcode':
                        field['value'] = flight_code
                    elif field['id'] == 'flightdate':
                        field['value'] = form.dateOfFlight.data.strftime('%Y-%m-%d')
                    elif field['id'] == 'description':
                        field['value'] = form.description.data
                    elif field['id'] == 'preparedby':
                        field['value'] = users_name

        site_evaluation_value = deepcopy(SiteEvaluationTemplate)

        for template in site_evaluation_value:
            for section in template['form']['sections']:
                for field in section['fields']:
                    if field['id'] == 'flightcode':
                        field['value'] = flight_code
                    elif field['id'] == 'dateofflight':
                        field['value'] = form.dateOfFlight.data.strftime('%Y-%m-%d')
                    elif field['id'] == 'remotepilot':
                        field['value'] = users_name

        # All valid, create new project
        project = Project(
            authorID=current_user.id,
            longitude=float(longitude),
            latitude=float(latitude),
            projectType=project_type,
            title=form.title.data,
            description=form.description.data,
            dateOfFlight=form.dateOfFlight.data,
            projectPurposeID=form.projectPurposeID.data,
            lastEdited=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            flightCode = flight_code,
            # JSON forms
            viabilityStudy = viability_study_value,
            siteEvaluation = site_evaluation_value
        )

        # Commit new record to db
        db.session.add(project)
        db.session.commit()

        # Clear session data
        session.pop('longitude', None)
        session.pop('latitude', None)
        session.pop('projectType', None)

        # Audit
        AuditLogger.log(current_user.id, 'new_project', f'Created project id: {project.id}')

        # Flash and redirect
        flash('Project created successfuly!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('/create_project/new_project_details.html', form=form, footer=False, title='Almost there...')


@app.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    # Fetch project by ID
    project = Project.query.get_or_404(project_id)

    # User is author?
    if project.author.id != current_user.id:
        flash("You are not authorised to edit this project.", "danger")
        return redirect(url_for('dashboard'))

    # Define the form for editing the project
    form = EditProject(obj=project)

    if form.validate_on_submit():
        # Update record form data
        project.title = form.title.data
        project.description = form.description.data
        project.lastEdited=datetime.now(timezone.utc)

        # Commit changes 
        db.session.commit()

        # Audit
        AuditLogger.log(current_user.id, 'edit_project', f'Edited project id: {project.id}')

        flash("Project updated successfully.", "success")
        return redirect(url_for('project', project_id=project.id)) 

    return render_template("dashboard/edit_project.html", form=form, project=project)


@app.route("/project/<int:project_id>/remove")
@login_required
def remove_project(project_id):
    # Query by id
    project = Project.query.get_or_404(project_id)

    # Check ownership
    if project.authorID != current_user.id:
        flash('You do not have permission to remove this project.', 'danger')
        return redirect(url_for('dashboard'))

    try:
        # delete project
        db.session.delete(project)

        # commits changes
        db.session.commit()

        # Audit
        AuditLogger.log(current_user.id, 'remove_project', f'Removed project id: {project.id}')

        # redirects user and flashes message
        flash("Project removed successfully.", "success")
        return redirect(url_for('projects'))

    except:
        # rolls back any uncommited changes as a precaution
        db.session.rollback()

        #  redirects user and flashes message
        flash("Project couldn't be removed at this time.", "danger")
        return redirect(url_for('project', project_id=project.id))

