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
            print("Form Saved")

        # submits completed form
        if form.submit.data and form.validate_on_submit():
            print("Form Submitted")

    return render_template("/forms/viability_study.html", form=form)

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