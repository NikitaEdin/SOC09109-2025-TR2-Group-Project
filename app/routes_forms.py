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

    placeholderMessages = {
        'locationInformation': {
            'placeholder': """ 
                · Elevation in feet above mean sea level 
                · 6-figure grid reference 
                · Address including postcode 
                · What3words could be useful in some instances
                            """,
        },
        'sensitivities': {

            'placeholder': """  
                This could include things like schools, cemeteries, government buildings where
                flying a drone in the vicinity could cause issues or concerns with the public.  
                This may help you to decide if it would be worth informing the police via 101
                            """,
        },
        'airspace': {
            'placeholder': """
                Example 1 – No ATC Permission required Class G airspace uncontrolled            
                Example 2 – No ATC Permission required, ATC Notification if deemed necessary   
                Class D airspace Leeds Bradford CTR – Surface – 4500ft amsl             
                Example 3 – ATC Permission required Leeds Bradford Flight restriction zone
                            """,
        },
    }

    return render_template("/forms/site_evaluation.html", placeholders = placeholderMessages)