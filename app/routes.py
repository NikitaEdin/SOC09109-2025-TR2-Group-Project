from app import app
from flask import render_template, request

from app.forms.viabilityStudyForm import ViabilityStudyForm
from app.models import User, Role


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/viability-study', methods=['GET', 'POST'])
def viability_study():
    form = ViabilityStudyForm()

    if request.method == "POST":
        # saves changes only for finalising later
        if form.saveChanges.data:
            print("Form Saved")

        # submits completed form
        if form.validate_on_submit() and form.submit.data:
            print("Form Submitted")

    return render_template("forms/viabilityStudy.html", form=form)


