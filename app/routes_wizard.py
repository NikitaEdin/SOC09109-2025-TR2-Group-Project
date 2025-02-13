from flask import render_template

from app import app


@app.route("/wizard/plot", methods=['GET', 'POST'])
def wizard_plot():
    return render_template('/wizard/plot.html')

# TODO: move these into a more sensible place
mandatory_checks = {
    'preflight_checks': {
        'title': 'Preflight Checks',
        'description': 'Drone Maintenance Etc.',
        'value': False
    },
    'postflight_checks': {
        'title': 'Postflight Checks',
        'description': 'Reviewing the flight data',
        'value': False
    },
    'site_checks': {
        'title': 'Site Checks',
        'description': 'Checking if the site is fit for purpose on the day',
        'value': False
    },
    'weather_eval': {
        'title': 'Weather Evaluation',
        'description': 'Checking if the weather conditions will affect the flight on the day',
        'value': False
    },
    'crew_briefing': {
        'title': 'Crew Briefing',
        'description': 'Briefing the crew on the flight plan',
        'value': False
    },
    'viability_study': {
        'title': 'Viability Study',
        'description': 'Checking if the flight is viable',
        'value': False
    },
    'site_eval': {
        'title': 'Site Evaluation',
        'description': 'Evaluate the site',
        'value': False
    },
    'risk_analysis': {
        'title': 'Risk Analysis',
        'description': 'Analyse the risk factors',
        'value': False
    },
}

optional_checks = {
    'leaflet_drop': {
        'title': 'Leaflet Drop',
        'description': 'Carry out a leaflet drop and/or a door-to-door advisory campaign if the flight operation is to take place in a highly populated area, such as a housing estate',
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
    },
    'customise_loading_list': {
        'title': 'Customise Loading List',
        'description': 'Customise the loading list to suit the flight operation',
        'value': False
    },
    'land_permission': {
        'title': 'Permission from Land Owner',
        'description': 'Obtain permission to land on the landowner’s property',
        'value': False
    }
}

@app.route("/wizard/populated_checklist", methods=['GET', 'POST'])
def wizard_populated_checklist():
    return render_template('/wizard/populated_checklist.html', mandatory_checks=mandatory_checks, optional_checks=optional_checks)


@app.route("/wizard/rural_checklist", methods=['GET', 'POST'])
def wizard_rural_checklist():
    return render_template('/wizard/rural_checklist.html', mandatory_checks=mandatory_checks, optional_checks=optional_checks)

@app.route("/wizard/create-rural", methods=['GET', 'POST'])
def wizard_create_project_rural():
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
    }
    
    return render_template('/wizard/create_project_rural.html', checks=checks)

@app.route("/wizard/create-urban", methods=['GET','POST'])
def wizard_create_project_urban():
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
    
    return render_template('/wizard/create_project_urban.html', checks=checks)

@app.route("/wizard/getting_started", methods=['GET', 'POST'])
def wizard_getting_started():
    return render_template('/wizard/getting_started.html')