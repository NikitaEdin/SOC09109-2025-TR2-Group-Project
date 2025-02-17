from app import app
from flask import render_template, request
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