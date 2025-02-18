from app import app
from flask import render_template, request

from app.forms.crewCallSheetForm import CrewCallSheetForm
from app.forms.viabilityStudyForm import ViabilityStudyForm

@app.route('/forms/viability-study', methods=['GET', 'POST'])
def viability_study():
    form = ViabilityStudyForm()

    if request.method == "POST":
        # saves changes only for finalising later
        if form.saveChanges.data:
            print("viability study form saved for later")

        # submits completed form
        if form.submit.data and form.validate_on_submit():
            print("viability study form submitted")

    return render_template("/forms/viability_study.html", form=form)

@app.route('/forms/site-evaluation', methods=['GET', 'POST'])
def site_evaluation():
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
@app.route("/forms/loading-list")
def loading_list():
    return render_template('forms/loading/loading_list.html', title='Loading List')

# Loading List CREW Form Route
@app.route("/forms/loading-list/crew")
def loading_list_crew():
    return render_template('forms/loading/crew.html', title='Loading List - Crew')

# Loading List EQUIPMENT Form Route
@app.route("/forms/loading-list/equipment")
def loading_list_equipment():
    return render_template('forms/loading/equipment.html', title='Loading List - Equipment')

# Loading List MAINTENANCE KIT Form Route
@app.route("/forms/loading-list/maintenance-kit")
def loading_list_maintenance_kit():
    return render_template('forms/loading/maintenance_kit.html', title='Loading List - Maintenance Kit')

# Loading List SAFETY KIT Form Route
@app.route("/forms/loading-list/safety-kit")
def loading_list_safety_kit():
    return render_template('forms/loading/safety_kit.html', title='Loading List - Safety Kit')

# Loading List GROUND EQUIPMENT Form Route
@app.route("/forms/loading-list/ground-equipment")
def loading_list_ground_equip():
    return render_template('forms/loading/ground_equipment.html', title='Loading List - Ground Equipment')