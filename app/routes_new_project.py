from datetime import datetime, timezone
from app import app, db
from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.forms.createProject import ProjectLocation, ProjectType, ProjectDetails
from app.models import Project

# Step 1: Get location of the project
@app.route("/create_project/location", methods=['GET','POST'])
@login_required
def new_project_location():
    form = ProjectLocation()
    
    session.pop('longitude', None)
    session.pop('altitude', None)
    session.pop('projectType', None)

    # on form submit
    if form.validate_on_submit():
        session['longitude'] = form.longitude.data
        session['altitude'] = form.altitude.data
        return redirect(url_for('new_project_type'))
    
    return render_template('/create_project/new_project_location.html', form=form, footer=False, title='Where?')

# Step 2: Get project type
@app.route("/create_project/type", methods=['GET','POST'])
@login_required
def new_project_type():
    form = ProjectType()

    # Was step 1 skipped?
    if not session.get('longitude') and not session.get('altitude'):
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

    if not session.get('longitude') and not session.get('altitude') and not session.get('projectType'):
        flash('Project creation steps were not completed correctly.', 'danger')
        return redirect(url_for('new_project_location'))

    if form.validate_on_submit():
        # Retrieve session data
        longitude = session.get('longitude')
        altitude = session.get('altitude')
        project_type = session.get('projectType')

        # Get dataOfFlight to correct format

        # All valid, create new project
        project = Project(
            authorID=current_user.id,
            longitude=float(longitude),
            altitude=float(altitude),
            projectType=project_type,
            title=form.title.data,
            description=form.description.data,
            dateOfFlight=form.dateOfFlight.data,
            lastEdited=datetime.now(timezone.utc)
        )

        # Commit new record to db
        db.session.add(project)
        db.session.commit()

        # Clear session data
        session.pop('longitude', None)
        session.pop('altitude', None)
        session.pop('projectType', None)

        # Flash and redirect
        flash('Project created successfuly!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('/create_project/new_project_details.html', form=form, footer=False, title='Almost there...')