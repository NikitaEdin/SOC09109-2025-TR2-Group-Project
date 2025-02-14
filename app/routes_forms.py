from app import app
from flask import render_template, request
from app.forms.viabilityStudyForm import ViabilityStudyForm

@app.route('/forms/viability-study', methods=['GET', 'POST'])
def viability_study():
    form = ViabilityStudyForm()

    if request.method == "POST":
        # saves changes only for finalising later
        if form.saveChanges.data:
            print("Form Saved")

        # submits completed form
        if form.submit.data and form.validate_on_submit():
            print("Form Submitted")

    return render_template("/forms/viability_study.html", form=form)

@app.route('/forms/optional', methods =['GET','POST'])
def optional():
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
    urban = request.args.get('urban', 'False')
    rural = request.args.get('rural', 'False')
    return render_template("/forms/optional_forms.html", checks=checks, forms=forms, urban=urban,rural=rural,IncidentsEmergencies=IncidentsEmergencies )