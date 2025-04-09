from copy import deepcopy
from datetime import datetime, timezone
import uuid
from werkzeug.utils import secure_filename
import os
from app import app, db
from flask import flash, redirect, render_template, send_from_directory, session, url_for, request, jsonify
from flask_login import current_user, login_required

from app.AuditLogger import AuditLogger
from app.forms.createProject import EditProject, ProjectLocation, ProjectType, ProjectDetails, ProjectToggles
from app.models import Project, ProjectFile, User

from app.forms.jsons.viabilityStudyTemplate import ViabilityStudyTemplate
from app.forms.jsons.siteEvaluationTemplate import SiteEvaluationTemplate
from app.forms.jsons.riskAnalysisTemplate import riskAnalysisTemplate
from app.forms.jsons.loadingListSafetyKitTemplate import LoadingListSafetyKitTemplate
from app.forms.jsons.loadingListMaintenanceKitTemplate import LoadingListMaintenanceKitTemplate
from app.forms.jsons.loadingListEquipmentTemplate import LoadingListEquipmentTemplate
from app.forms.jsons.postFlightTemplate import PostFlightTemplate
from app.forms.jsons.loadingListCrewListTemplate import LoadingListCrewListTemplate
from app.forms.jsons.loadingListGroundEquipmentTemplate import LoadingListGroundEquipmentTemplate

UPLOAD_FOLDER = 'uploads/'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'ppt', 'pptx', 'txt', 'png', 'jpg', 'jpeg'}
MAX_FILES_PER_PROJECT = 10

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
        return redirect(url_for('new_project_type'))

    if form.validate_on_submit():
        session['projectTitle'] = form.title.data
        session['projectDescription'] = form.description.data
        session['projectDateOfFlight'] = form.dateOfFlight.data.strftime('%Y-%m-%d')
        session['projectPurposeID'] = form.projectPurposeID.data

        return redirect(url_for('new_project_toggles'))

    return render_template('/create_project/new_project_details.html', form=form, footer=False, title='Almost there...')

# Step 4: Set project toggles, what document are not required
@app.route("/create_project/toggles", methods=['GET','POST'])
@login_required
def new_project_toggles():
    form = ProjectToggles()

    if not session.get('projectTitle') or not session.get('projectDescription') or not session.get('projectDateOfFlight') or not session.get('projectPurposeID'):
        flash('Project creation steps were not completed correctly.', 'danger')
        return redirect(url_for('new_project_details'))


    if form.validate_on_submit():
        # Retrieve session data
        longitude = session.get('longitude')
        latitude = session.get('latitude')
        project_type = session.get('projectType')

        title = session.get('projectTitle')
        description = session.get('projectDescription')
        date_of_flight = datetime.strptime(session.get('projectDateOfFlight'), '%Y-%m-%d')
        project_purose_id = session.get('projectPurposeID')

        # Get dataOfFlight to correct format

        # prepopulate form
        users_name = current_user.username

        if current_user.displayname:
            users_name = current_user.displayname

        flight_code = Project.get_new_flightCode(project_purose_id)

        viability_study_value = deepcopy(ViabilityStudyTemplate)

        for template in viability_study_value:
            for section in template['form']['sections']:
                for field in section['fields']:
                    if field['id'] == 'flightcode':
                        field['value'] = flight_code
                    elif field['id'] == 'flightdate':
                        field['value'] = date_of_flight.strftime('%Y-%m-%d')
                    elif field['id'] == 'description':
                        field['value'] = description
                    elif field['id'] == 'preparedby':
                        field['value'] = users_name

        site_evaluation_value = deepcopy(SiteEvaluationTemplate)

        for template in site_evaluation_value:
            for section in template['form']['sections']:
                for field in section['fields']:
                    if field['id'] == 'flightcode':
                        field['value'] = flight_code
                    elif field['id'] == 'dateofflight':
                        field['value'] = date_of_flight.strftime('%Y-%m-%d')
                    elif field['id'] == 'remotepilot':
                        field['value'] = users_name

        togglesJSON = {
            'loadingListRequired': form.loadingListRequired.data,
            'protectedAreaFlight': form.protectedAreaFlight.data,
            'notamRequired': form.notamRequired.data,
            'leafletDropRequired': form.leafletDropRequired.data,
            'localClubNearby': form.localClubNearby.data,
            'permissionRequired': form.permissionRequired.data
        }

        # All valid, create new project
        project = Project(
            authorID=current_user.id,
            longitude=float(longitude),
            latitude=float(latitude),
            projectType=project_type,
            title=title,
            description=description,
            dateOfFlight=date_of_flight,
            projectPurposeID=project_purose_id,
            lastEdited=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            flightCode = flight_code,
            # JSON forms
            viabilityStudy = viability_study_value,
            siteEvaluation = site_evaluation_value,
            riskAnalysis = riskAnalysisTemplate[0],
            toggles = togglesJSON,
           
            
            # Loading list
            postFlight = PostFlightTemplate,
            safetyKit = LoadingListSafetyKitTemplate,
            maintenanceKit = LoadingListMaintenanceKitTemplate,
            equipment = LoadingListEquipmentTemplate,
            groundEquipment = LoadingListGroundEquipmentTemplate,
            crewList = LoadingListCrewListTemplate
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

    # Disable items based on type
    if (session.get('projectType') == 'Rural'):
        form.leafletDropRequired.render_kw = {'disabled': 'disabled'}

    return render_template('/create_project/new_project_toggles.html', form=form, footer=False, title='Final steps...')

@app.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    # Fetch project by ID
    project = Project.query.get_or_404(project_id)

    # Can edit (original author or admin, NOT shared project)
    if not project.can_edit():
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

    # Can edit (original author or admin, NOT shared project)
    if not project.can_edit():
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


@app.route('/project/<int:project_id>/manage_access', methods=['GET', 'POST'])
@login_required
def manage_access(project_id):
    project = Project.query.get_or_404(project_id)

    # Ensure only the author can manage access
    # Can edit (original author or admin, NOT shared project)
    if not project.can_edit():
        flash("You do not have permission to manage this project's access.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        action = request.form.get('action')

        user = User.query.get(user_id)

        if user:
            if action == "add" and user not in project.allowed_users:
                project.allowed_users.append(user)
                flash(f"User {user.username} added.", "success")
            elif action == "remove" and user in project.allowed_users:
                project.allowed_users.remove(user)
                flash(f"User {user.username} removed.", "warning")
            db.session.commit()

    return render_template('dashboard/manage_access.html', project=project)

@app.route('/search_users', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('query')
    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])



############################ PROJECT FILES ############################
# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/project/<int:project_id>/files', methods=['GET'])
@login_required
def project_files(project_id):
    project = Project.query.get_or_404(project_id)

    # Can access?
    if not project.can_access():
        flash("You are not authorised to edit this project.", "danger")
        return redirect(url_for('dashboard'))

    return render_template('/dashboard/project_files.html', project=project, footer=False,
        max_file_size=MAX_FILE_SIZE, 
        allowed_extensions=ALLOWED_EXTENSIONS, 
        max_files=MAX_FILES_PER_PROJECT)


@app.route('/project/<int:project_id>/files/upload', methods=['POST'])
@login_required
def upload_file(project_id):
    project = Project.query.get_or_404(project_id)

    # Can edit
    if not project.can_edit():
        flash("You are not authorised to edit this project.", "danger")
        return redirect(url_for('dashboard'))
    
    # Max number of files per project
    if len(project.files) >= MAX_FILES_PER_PROJECT:
        flash(f"Maximum of {MAX_FILES_PER_PROJECT} files allowed.", "danger")
        return redirect(url_for('project_files', project_id=project_id))

    file = request.files.get('file')

    # No file
    if not file or file.filename == '':
        flash("No file selected!", "danger")
        return redirect(url_for('project_files', project_id=project_id))

    # Allowed file
    if not allowed_file(file.filename):
        flash(f"Invalid file type! Allowed types: {', '.join(ALLOWED_EXTENSIONS)}", "danger")
        return redirect(url_for('project_files', project_id=project_id))

    original_filename = secure_filename(file.filename)

    # Check if file with the same name already exists
    existing_file = ProjectFile.query.filter_by(project_id=project.id, original_filename=original_filename).first()

    if existing_file:
        # Delete old file before replacing
        if os.path.exists(existing_file.filepath):
            os.remove(existing_file.filepath)

        # Keep same database entry but update filename and path
        unique_filename = f"{project_id}_{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save and update record
        file.save(filepath)

        existing_file.filename = unique_filename
        existing_file.filepath = filepath
        existing_file.size = os.path.getsize(filepath)
        existing_file.uploaded_at = datetime.utcnow()
        db.session.commit()

        flash("File replaced successfully!", "success")
    else:
        # New file upload (<ProjectID>_<UUID>_<filename>)
        unique_filename = f"{project_id}_{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Ensure folder exists and save
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
        file.save(filepath)

        new_file = ProjectFile(
            filename=unique_filename,
            original_filename=original_filename,
            filepath=filepath,
            size=os.path.getsize(filepath),
            project_id=project.id
        )
        db.session.add(new_file)
        db.session.commit()

        flash("File uploaded successfully!", "success")

    return redirect(url_for('project_files', project_id=project_id))


@app.route('/project/<int:project_id>/files/<int:file_id>/download')
@login_required
def download_file(project_id, file_id):
    file = ProjectFile.query.get_or_404(file_id)

    # File belongs to project the user has access
    if not file.project.can_access():
        flash("You are not authorised to download this file.", "danger")
        return redirect(url_for('dashboard'))

    directory = os.path.abspath(UPLOAD_FOLDER)
    return send_from_directory(directory, file.filename, as_attachment=True, download_name=file.original_filename)


@app.route('/project/<int:project_id>/files/<int:file_id>/delete', methods=['POST'])
@login_required
def delete_file(project_id, file_id):
    file = ProjectFile.query.get_or_404(file_id)

     # File belongs to project the user has access
    if not file.project.can_edit():
        flash("You are not authorised to delete this file.", "danger")
        return redirect(url_for('dashboard'))

    if os.path.exists(file.filepath):
        os.remove(file.filepath)

    db.session.delete(file)
    db.session.commit()
    
    flash("File deleted successfully!", "success")
    return redirect(url_for('project_files', project_id=project_id))