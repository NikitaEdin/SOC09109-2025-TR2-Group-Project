from flask_login import login_required
from app import app, db
from flask import flash, json, redirect, render_template, request, url_for
from sqlalchemy.orm.attributes import flag_modified
from app.forms.crewCallSheetForm import CrewCallSheetForm
from app.forms.jsons.viabilityStudyTemplate import ViabilityStudyTemplate
from app.models import Project
from app.routes_auth import requires_admin

from datetime import datetime

def is_valid_date(date_str):
    try:
        # Try to parse the date in YYYY-MM-DD format
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@app.route("/project/<int:project_id>/viability-study", methods=["GET", "POST"])
@login_required
@requires_admin
def viability_study(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.viabilityStudy    
    errors = {}  # validation errors
    
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                field_id = field['id']  
                field_value = request.form.get(field_id)

                # Validation for flightcode (example)
                if field_id == 'flightcode':
                    if not field_value:
                        errors[field_id] = "Flight code is required."
                    elif not field_value.isnumeric():  # Must be numeric
                        errors[field_id] = "Flight code must be numeric."

              

                # If the field passes validation, save its value back to the JSON
                if field_id not in errors:
                    field['value'] = field_value  # Update the field value with the submitted value

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/viability_study.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.viabilityStudy = form_data
        flag_modified(project, "viabilityStudy")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('project', project_id=project.id))
    
    return render_template("/forms/viability_study.html", project=project, form_data=form_data, footer=False, title="Viability Study")

@app.route("/project/<int:project_id>/viability-study/export", methods=["GET"])
@login_required
def export_viability_study(project_id):
    project = Project.query.get_or_404(project_id)

    return render_template("/forms/export.html", form_data=project.viabilityStudy, title="Viability Study")

@app.route('/project/<int:project_id>/site-evaluation', methods=['GET', 'POST'])
@login_required
def site_evaluation(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.siteEvaluation    
    errors = {}  # validation errors
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            try:
                for field in section['fields']:
                    field_id = field['id']  
                    field_value = request.form.get(field_id)

                    # Any field validations go here, before it's assigned
                    if field_id not in errors:
                        field['value'] = field_value
            except:
                pass
                

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/site-evaluation.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.siteEvaluation = form_data
        flag_modified(project, "siteEvaluation")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('project', project_id=project.id))
    
    return render_template("/forms/site_evaluation.html", project=project, form_data=form_data, footer=False, title="Site Evaluation")


@app.route("/project/<int:project_id>/site-evaluation/export", methods=["GET"])
@login_required
def export_site_evaluation(project_id):
    project = Project.query.get_or_404(project_id)

    return render_template("/forms/export.html", form_data=project.siteEvaluation, title="Site Evaluation")


@app.route('/forms/site-evaluation-template', methods=['GET', 'POST'])
def site_evaluation_template():
    return render_template("/forms/site_evaluation_copy.html")

@app.route('/project/<int:project_id>/crew_call_sheet', methods=['GET', 'POST'])
@login_required
def crew_call_sheet(project_id):
    form = CrewCallSheetForm()

    # save & submit handler
    if request.method == "POST":
        if form.saveChanges.data:
            print("Form Saved")

        if form.submit.data and form.validate_on_submit():
            print("Form Submitted")

    return render_template("/forms/crew_call_sheet.html", form=form)

# Post Flight Actions Form Route
@app.route("/project/<int:project_id>/post-flight")
@login_required
def post_flight(project_id):
    return render_template('forms/post_flight.html', title='Post-Flight Actions')

# Risk Analysis Form
# template missing ###################################################################
@app.route("/project/<int:project_id>/risk-analysis")
@login_required
def risk_analysis(project_id):
    return render_template('forms/risk_analysis/risk_analysis_list.html', title=' Risk Analysis Form')

# Risk Analysis Form - Add Risk Route
@app.route("/project/<int:project_id>/risk-analysis/add")
@login_required
def add_risk_analysis(project_id):
    return render_template('forms/risk_analysis/add_risk.html', title='Add Risk Analysis Form')

# Loading List Route
@app.route("/project/<int:project_id>/loading-list")
@login_required
def loading_list(project_id):
    return render_template('forms/loading/loading_list.html', title='Loading List', project_id=project_id)

# Loading List CREW Form Route
@app.route("/project/<int:project_id>/loading-list/crew")
@login_required
def loading_list_crew(project_id):
    return render_template('forms/loading/crew.html', title='Loading List - Crew', project_id=project_id)

# Loading List EQUIPMENT Form Route
@app.route("/project/<int:project_id>/loading-list/equipment")
@login_required
def loading_list_equipment(project_id):
    return render_template('forms/loading/equipment.html', title='Loading List - Equipment', project_id=project_id)

# Loading List MAINTENANCE KIT Form Route
@app.route("/project/<int:project_id>/loading-list/maintenance-kit")
@login_required
def loading_list_maintenance_kit(project_id):
    return render_template('forms/loading/maintenance_kit.html', title='Loading List - Maintenance Kit', project_id=project_id)

# Loading List SAFETY KIT Form Route
@app.route("/project/<int:project_id>/loading-list/safety-kit")
@login_required
def loading_list_safety_kit(project_id):
    return render_template('forms/loading/safety_kit.html', title='Loading List - Safety Kit', project_id=project_id)

# Loading List GROUND EQUIPMENT Form Route
@app.route("/project/<int:project_id>/loading-list/ground-equipment")
@login_required
def loading_list_ground_equip(project_id):
    return render_template('forms/loading/ground_equipment.html', title='Loading List - Ground Equipment', project_id=project_id)