from flask_login import login_required
from app import app, db
from flask import flash, json, redirect, render_template, request, url_for
from sqlalchemy.orm.attributes import flag_modified
from app.forms.crewCallSheetForm import CrewCallSheetForm
from app.forms.jsons.viabilityStudyTemplate import ViabilityStudyTemplate
from app.forms.jsons.loadingListSafetyKitTemplate import LoadingListSafetyKitTemplate
from app.forms.jsons.loadingListMaintenanceKitTemplate import LoadingListMaintenanceKitTemplate
from app.models import Project

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

    """
    form = siteEvaluationForm()

    if request.method == "POST":
        # saves changes only for finalising later
        if form.saveChanges.data:
            print("site evaluation form saved for later")

        # submits completed form
        if form.submit.data and form.validate_on_submit():
            print("site evaluation form submitted")
    """

    return render_template("/forms/site_evaluation.html")


@app.route("/project/<int:project_id>/site-evaluation/export", methods=["GET"])
@login_required
def export_site_evaluation(project_id):
    project = Project.query.get_or_404(project_id)

    return render_template("/forms/export.html", form_data=project.siteEvaluation, title="Site Evaluation")


@app.route('/forms/site-evaluation-template', methods=['GET', 'POST'])
def site_evaluation_template():
    return render_template("/forms/site_evaluation_copy.html")

@app.route('/forms/crew_call_sheet', methods=['GET', 'POST'])
def crew_call_sheet():
    form = CrewCallSheetForm()

    # save & submit handler
    if request.method == "POST":
        if form.saveChanges.data:
            print("Form Saved")

        if form.submit.data and form.validate_on_submit():
            print("Form Submitted")

    return render_template("/forms/crew_call_sheet.html", form=form)

# Post Flight Actions Form Route
@app.route("/forms/post-flight")
def post_flight():
    return render_template('forms/post_flight.html', title='Post-Flight Actions')

# Risk Analysis Form 
@app.route("/forms/risk-analysis")
def risk_analysis():
    return render_template('forms/risk_analysis/risk_analysis_list.html', title=' Risk Analysis Form')

# Risk Analysis Form - Add Risk Route
@app.route("/forms/risk-analysis/add")
def add_risk_analysis():
    return render_template('forms/risk_analysis/add_risk.html', title='Add Risk Analysis Form')

# Loading List Route
@app.route("/project/<int:project_id>/loading-list")
def loading_list(project_id):
    project = Project.query.get_or_404(project_id)

    form_maintenanceKit = project.maintenanceKit  
    form_safetyKit = project.safetyKit
    form_equipment = project.equipment 
    form_groundEquipment = project.groundEquipment
    form_crewList = project.crewList 
    
    # Loop through each section
    for section in form_maintenanceKit[0]['form']['sections']:
         # Loop through all fields
         for field in section['fields']:
            if field['value']:
                form_maintenanceKitStatus = True
            else:
                form_maintenanceKitStatus = False
                
    # Loop through each section
    for section in form_safetyKit[0]['form']['sections']:
         # Loop through all fields
         for field in section['fields']:
            if field['value']:
                form_safetyKitStatus = True
            else:
                form_safetyKitStatus = False
                
    # Loop through each section
    for section in form_equipment[0]['form']['sections']:
         # Loop through all fields
         for field in section['fields']:
            if field['value']:
                form_equipmentStatus = True
            else:
                form_equipmentStatus = False
                
    # Loop through each section
    for section in form_groundEquipment[0]['form']['sections']:
         # Loop through all fields
         for field in section['fields']:
            if field['value'] != None and field['value'] == True:
                form_groundEquipmentStatus = True
            else:
                form_groundEquipmentStatus = False
               
    # Loop through each section
    for section in form_crewList[0]['form']['sections']:
         # Loop through all fields
         for field in section['fields']:
            if field['value'] != None and  field['value'] == True:
                form_crewListStatus = True
            else:
                form_crewListStatus = False
                
    form_status = {
    "form_maintenanceKitStatus": form_maintenanceKitStatus,
    "form_safetyKitStatus": form_safetyKitStatus,
    "form_equipmentStatus": form_equipmentStatus,
    "form_groundEquipmentStatus": form_groundEquipmentStatus,
    "form_crewListStatus": form_crewListStatus
}
    return render_template('forms/loading/loading_list.html', title='Loading List', project=project, form_status=form_status, footer=False)

# Loading List CrewList Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/crew-list", methods=["GET", "POST"])
@login_required
def loading_list_crew(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.crewList    
    errors = {}  # validation errors
    
    if request.method == 'POST':

        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            try:
                for field in section['fields']:
                    field_id = field['id']  
                    field_value = request.form.get(field_id)

                    # Any field validations go here, before it's assigned
                    if field_id not in errors:
                        field['value'] = field_value
                
                    # Handle checkboxes 
                    if field['type'] == 'checkbox':  
                        field['value'] = request.form.get(field_id) == "on"  # True if checked
            except:
                pass 
               
        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/crew_list_json.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.crewList = form_data
        flag_modified(project, "crewList")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('loading_list', project_id=project.id))
    
    return render_template("/forms/loading/crew_list_json.html", project=project, form_data=form_data, footer=False, title="Crew List" )

# Loading List EQUIPMENT KIT Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/equipment", methods=["GET", "POST"])
@login_required
def loading_list_equipment(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.equipment    
    errors = {}  # validation errors
    
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                field_id = field['id']  
               
                # Handle checkboxes 
                if field['type'] == 'checkbox':  
                    field['value'] = request.form.get(field_id) == "on"  # True if checked
                else:
                    field['value'] = False

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/equipment_json.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.equipment = form_data
        flag_modified(project, "equipment")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('loading_list', project_id=project.id))
    
    return render_template("/forms/loading/equipment_json.html", project=project, form_data=form_data, footer=False, title="Equipment" )

# Loading List MAINTENANCE KIT Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/maintenance-kit", methods=["GET", "POST"])
@login_required
def loading_list_maintenance_kit(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.maintenanceKit    
    errors = {}  # validation errors
    
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                field_id = field['id']  
               
                # Handle checkboxes 
                if field['type'] == 'checkbox':  
                    field['value'] = request.form.get(field_id) == "on"  # True if checked
                else:
                    field['value'] = False

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/maintenance_kit_json.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.maintenanceKit = form_data
        flag_modified(project, "maintenanceKit")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('loading_list', project_id=project.id))
    
    return render_template("/forms/loading/maintenance_kit_json.html", project=project, form_data=form_data, footer=False, title="Maintenance Kit" )

# Loading List SAFETY KIT Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/safety-kit", methods=["GET", "POST"])
@login_required
def loading_list_safety_kit(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.safetyKit    
    errors = {}  # validation errors
    
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            try:
                for field in section['fields']:
                    field_id = field['id']  
                    field_value = request.form.get(field_id)

                 # Handle checkboxes first 
                if field['type'] == 'checkbox':
                    field['value'] = request.form.get(field_id) == "on"  # True if checked
                else:
                    # For other fields 
                    if field_id not in errors:
                        field['value'] = field_value #
            except:
                pass 

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/safety_kit_json.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.safetyKit = form_data
        flag_modified(project, "safetyKit")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('loading_list', project_id=project.id))
    
    return render_template("/forms/loading/safety_kit_json.html", project=project, form_data=form_data, footer=False, title="Safety Kit" )


# @app.route("/project/<int:project_id>/loading-list/ground-equipment")
# def loading_list_ground_equip(project_id):
#     project = Project.query.get_or_404(project_id)
#     return render_template('forms/loading/ground_equipment.html', title='Loading List - Ground Equipment', project=project, project_id=project_id, footer=False)

# Loading List GROUND EQUIPMENT JSON Form Route
@app.route("/project/<int:project_id>/loading-list/ground-equipment", methods=["GET", "POST"])
@login_required
def loading_list_ground_equip(project_id):
    project = Project.query.get_or_404(project_id)
    form_data = project.groundEquipment    
    errors = {}  # validation errors
    
    if request.method == 'POST':

        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            try:
                for field in section['fields']:
                    field_id = field['id']  
                    field_value = request.form.get(field_id)

                 # Handle checkboxes first 
                if field['type'] == 'checkbox':
                    field['value'] = request.form.get(field_id) == "on"  # True if checked
                else:
                    # For other fields 
                    if field_id not in errors:
                        field['value'] = field_value #
            except:
                pass 
               
        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/ground_equipment_json.html', project=project, form_data=form_data, errors=errors)

        # No errors, save changes
        project.groundEquipment = form_data
        flag_modified(project, "groundEquipment")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return redirect(url_for('loading_list', project_id=project.id))
    
    return render_template("/forms/loading/ground_equipment_json.html", project=project, form_data=form_data, footer=False, title="Ground Equipment" )