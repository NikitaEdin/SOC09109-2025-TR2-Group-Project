from flask import render_template, request

from app import app
from app.models import db, Project, checklist_template

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

@app.route('/create_project/optional', methods =['GET','POST'])
def optional():
    
    # TODO Return to this should grab the project based on the id passed on from the dashboard
    # project = Project.query.get_or_404(project_id)
    
    # if not project.checklist:
    #     project.checklist = []
    #     for item in checklist_template:
    #         project.checklist.append({
    #             "name": item["name"],
    #             "status": False,
    #             "last_edit": None
    #         })
    #     db.session.commit()
        
    checks={
        'leaflet_drop': {
        'title': 'Leaflet Drop',
        'description': 'Carry out a leaflet drop and/or a door-to-door advisory campaign',
        'value': False
    },
    'inform_police': {
        'title': 'Inform Police',
        'description': 'Inform the local police if the planned flight operation is to take place in areas where there is likely to be members of the public',
        'value': False
    },
    'inform_local_air_user': {
        'title': 'Inform Local Air Users',
        'description': 'If there is a local air user club nearby, contact the club and enquire about any likely activity on the day of the proposed flight operation',
        'value': False
    },
    'monitor_weather': {
        'title': 'Monitor Weather',
        'description': 'Monitor the weather conditions on the day of the proposed flight operation',
        'value': False
    }
    }
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
    "IncidentsEmergencies": IncidentsEmergencies,
    "urban": request.args.get('urban', 'False'),
    "rural": request.args.get('rural', 'False')
}
    return render_template("create_project/optional_forms.html", content=content )
