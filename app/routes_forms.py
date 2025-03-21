from re import match

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
    
def security():
       if not project.can_access():
        flash("You are not authorised to access this project.", "danger")
        return redirect(url_for('dashboard'))

@app.route("/project/<int:project_id>/viability-study", methods=["GET", "POST"])
@login_required
def viability_study(project_id):
    project = Project.query.get_or_404(project_id)
    security()
    
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
                    elif not match(r"[A-z][0-9]+", field_value):  # Must follow the pattern of a letter followed by numbers
                        errors[field_id] = "Flight code must follow the format A123."

              

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
    security()

    return render_template("/forms/export.html", form_data=project.viabilityStudy, title="Viability Study")

@app.route('/project/<int:project_id>/site-evaluation', methods=['GET', 'POST'])
@login_required
def site_evaluation(project_id):
    project = Project.query.get_or_404(project_id)
    security()
    
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

                    if field_id == 'flightcode':
                        if not field_value:
                            errors[field_id] = "Flight code is required."
                        elif not match(r"[A-z][0-9]+", field_value):  # Must follow the pattern of a letter followed by numbers
                            errors[field_id] = "Flight code must follow the format A123."

                    # Any field validations go here, before it's assigned
                    if field_id not in errors:
                        field['value'] = field_value
            except:
                pass
                

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/site_evaluation.html', project=project, form_data=form_data, errors=errors)

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
    security()

    return render_template("/forms/export.html", form_data=project.siteEvaluation, title="Site Evaluation")


@app.route('/forms/site-evaluation-template', methods=['GET', 'POST'])
def site_evaluation_template():
    return render_template("/forms/site_evaluation_copy.html")

@app.route('/project/<int:project_id>/crew_call_sheet', methods=['GET', 'POST'])
@login_required
def crew_call_sheet(project_id):
    project = Project.query.get_or_404(project_id)
    security()

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
    project = Project.query.get_or_404(project_id)
    security()

    return render_template('forms/post_flight.html', title='Post-Flight Actions')

# Risk Analysis Form
@app.route("/project/<int:project_id>/risk-analysis")
@login_required
def risk_analysis(project_id):
    project = Project.query.get_or_404(project_id)
    security()

    return render_template('forms/risk_analysis/risk_analysis_list.html', title=' Risk Analysis Form')

# Risk Analysis Form - Add Risk Route
@app.route("/project/<int:project_id>/risk-analysis/add")
@login_required
def add_risk_analysis(project_id):
    project = Project.query.get_or_404(project_id)
    security()

    return render_template('forms/risk_analysis/add_risk.html', title='Add Risk Analysis Form')

# Loading List Route
@app.route("/project/<int:project_id>/loading-list")
def loading_list(project_id):
    project = Project.query.get_or_404(project_id)
    security()

    form_maintenanceKit = project.maintenanceKit  
    form_safetyKit = project.safetyKit
    form_equipment = project.equipment 
    
    # By default, assume all are incomplete
    form_maintenanceKitStatus = False
    form_safetyKitStatus = False
    form_equipmentStatus = False
    form_groundEquipmentStatus = False
    form_crewListStatus = False


    try:
        # Loop through each section
        for section in form_maintenanceKit[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                if field['value']:
                    form_maintenanceKitStatus = True
    except:
        pass

    try:
        # Loop through each section
        for section in form_safetyKit[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                if field['value']:
                    form_safetyKitStatus = True
    except:
        pass

    try:
        # Loop through each section
        for section in form_equipment[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                if field['value']:
                    form_equipmentStatus = True
    except:
        pass


    form_crewListStatus = calculate_status(project.crewList[0]['user_data'], field_name='called')
    form_groundEquipmentStatus = calculate_status(project.groundEquipment[0]['user_data'], field_name='check')

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
    security()
    
    form_data = project.crewList    
   
    
    if request.method == 'POST':
        
        user_data = []
        crew_names = request.form.getlist('crew_name[]')
        roles = request.form.getlist('role[]')
        contact_numbers = request.form.getlist('contact_number[]')
        emails = request.form.getlist('email[]')
        called_list = request.form.get('called', '')
        called_values = called_list.split(',') if called_list else []

        for i in range(len(crew_names)):
            called_value = (i < len(called_values)) and (called_values[i] == "true")

            # Append valid data to user_data
            user_data.append({
                "crew_name": crew_names[i].strip(),
                "role": roles[i].strip(),
                "contact_number": contact_numbers[i].strip() if contact_numbers[i] else "",
                "email": emails[i].strip() if emails[i] else "",
                "called": called_value
            })
        

        
        form_data[0]["user_data"] = user_data  # Update `user_data` array
        project.crewList = form_data
        flag_modified(project, "crewList")  
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        # return redirect(url_for('loading_list', project_id=project.id))
        return render_template("/forms/loading/crew_list_json.html", project=project, form_data=form_data, footer=False, title="Crew List" )
    
    
    return render_template("/forms/loading/crew_list_json.html", project=project, form_data=form_data, footer=False, title="Crew List" )

# Loading List EQUIPMENT KIT Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/equipment", methods=["GET", "POST"])
@login_required
def loading_list_equipment(project_id):
    project = Project.query.get_or_404(project_id)  
    security()
    
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
    security()
    
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
    security()
    
    form_data = project.safetyKit    
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
    security()
    
    form_data = project.groundEquipment    
   
    
    if request.method == 'POST':
        
        user_data = []
        items = request.form.getlist('item[]')
        actions = request.form.getlist('action[]')
        called_list = request.form.get('check', '')
        called_values = called_list.split(',') if called_list else []

        print(called_list)
        for i in range(len(items)):
            called_value = (i < len(called_values)) and (called_values[i] == "true")

            # Append valid data to user_data
            user_data.append({
                "item": items[i].strip(),
                "action": actions[i].strip(),
                "check": called_value
            })
        
        form_data[0]["user_data"] = user_data  # Update `user_data` array
        project.groundEquipment = form_data
        flag_modified(project, "groundEquipment")  
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
        return render_template("/forms/loading/ground_equipment_json.html", project=project, form_data=form_data, footer=False, title="Ground Equipment" )
    
    
    return render_template("/forms/loading/ground_equipment_json.html", project=project, form_data=form_data, footer=False, title="Ground Equipment" )


####################### UTILS #######################

# Calculate the status based on the values of given field, in given user_data section of JSON.
def calculate_status(user_data, field_name='called'):
    total_items = len(user_data)
    
    if total_items == 0:
        return 0  # No data, "Not Started"
    
    true_count = sum(1 for section in user_data if section.get(field_name) is True)
    print(true_count)
    print(total_items)
    if true_count == total_items:
        return 2  # All True (Complete)
    elif true_count > 0:
        return 1  # At least one True (In Progress)
    else:
        return 0  # No True values (Not Started)
