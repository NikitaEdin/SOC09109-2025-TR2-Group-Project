from datetime import datetime
from flask import render_template, request,redirect,url_for

from app import app
from app.models import db, Project, checklist_template_optional,checklist_template

@app.route("/create_project/create-rural", methods=['GET', 'POST'])
def create_project_rural():
    checks = {
         'viability_study': {
            'title': 'Complete Viability Study',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'site_eval': {
            'title': 'Complete Site Evaluation',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'loading_list': {
            'title': 'Loading List',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'risk_analysis':{
            'title': 'Risk Analysis',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'post_flight':{
            'title': 'Post Flight',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        }
    }
    
    return render_template('create_project/create_project_rural.html', checks=checks)

@app.route("/create_project/create-urban", methods=['GET','POST'])
def create_project_urban():
    checks = {
        'viability_study': {
            'title': 'Complete Viability Study',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'site_eval': {
            'title': 'Complete Site Evaluation',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'loading_list': {
            'title': 'Loading List',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'risk_analysis':{
            'title': 'Risk Analysis',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'post_flight':{
            'title': 'Post Flight',
            'description': 'Complete the form and checkbox ticks',
            'value': False
        },
        'advanced_flight':{
            'title':'Advanced Flight Permission',
            'description':'This is to apply to fly in restricted areas',
            'value': False
        }    
    }
    
    return render_template('create_project/create_project_urban.html', checks=checks)

@app.route('/create_project/optional/<int:project_id>', methods =['GET','POST'])
def optional(project_id):
    
    # TODO Return to this should grab the project based on the id passed on from the dashboard
    project = Project.query.get_or_404(project_id)
    
    # Checks if the checklist is generated if not give it default values
    if not project.checklist:
        project.checklist = []
        for item in checklist_template_optional:
            project.checklist.append({
                "name": item["name"],
                "status": False,
                "last_edit": None
            })
        db.session.commit()
        
    # Stores information from the checklist template
    checks={
        item["name"]: {
        "title": item["name"],
        "description": item["description"],
        "value": any(check["name"] == item["name"] and check["status"] for check in project.checklist),
        "last_edit": next((check["last_edit"] for check in project.checklist if check["name"] == item["name"]), None)
    } for item in checklist_template_optional
    }
    
    # On form submission checks if the checkbox is marked  then puts it into updated checklist
    if request.method == "POST":
        updated_checklist = []
        for item in project.checklist:
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            old_status = updated_item["status"]

            updated_item["status"] = status
            
            # Update only if the status changed
            if old_status != status:
                updated_item["last_edit"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        # Add any missing items from the checklist template
        project.update_checklist_from_json(updated_checklist)
        
        return redirect(url_for('optional', project_id=project.id))
    forms={
        'customise_loading_list': {
        'title': 'Customise Loading List',
        'description': 'Customise the loading list to suit the flight operation',
        'value': False
    },
    'land_permission': {
        'title': 'Permission from Land Owner',
        'description': 'Obtain permission to land on the landowner’s property',
        'value': False
    },
    'crew_call_sheets':{
        'title': 'Prepare and send Crew Call Sheets',
        'description' : 'Items for crew to bring on flight',
        'value': False

    },
    'post_flight_check':{
        'title': 'Post Flight Form',
        'description':'Form for post flight data',
        'value': False
    },
    'pre_flight_check':{
        'title':'Pre flight form',
        'description': 'Form for pre flight data',
        'value': False
    },
    'notam_form':{
        'title':'Notam Form',
        'description': 'Enter details into form',
        'value': False
    }
    }
    IncidentsEmergencies={
        'ECCAIRS':{
            'title': 'ECCAIRS Incident Link',
            'description': 'Click the button & fill the form',
            'value': False
        },
        'AIRPROX':{
            'title': 'AIRPROX Incident Link',
            'description':'Click the button & fill the form',
            'value': False
        }
    }
    
    

#  This is to tidy up and only pass in only one variable into the template
    content = {
    "checks": checks,
    "forms": forms,
    "IncidentsEmergencies": IncidentsEmergencies
}
    return render_template("create_project/optional_forms.html", content=content, project=project )
