from flask import render_template, request

from app import app


@app.route("/wizard/plot", methods=['GET', 'POST'])
def wizard_plot():
    return render_template('/wizard/plot.html')

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
        },
        'advanced_flight':{
            'title':'Advanced Flight Permission',
            'description':'This is to apply to fly in restricted areas',
            'value': False
        }    
    }
    
    return render_template('/wizard/create_project_urban.html', checks=checks)

@app.route("/wizard/getting_started", methods=['GET', 'POST'])
def wizard_getting_started():
    return render_template('/wizard/getting_started.html')