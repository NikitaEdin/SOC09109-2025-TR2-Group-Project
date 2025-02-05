from app import app
from flask import render_template
from app.models import User, Role


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home')


########## INFORMATIONAL PAGES ###########
@app.route("/privacy-policy")
def privacy():
    return render_template('/info/privacy_policy.html', title='Privacy Policy') 

@app.route("/terms-of-service")
def terms_of_service():
    return render_template('/info/terms_of_service.html', title='Terms of Service') 

@app.route("/contact-us")
def contact_us():
    return render_template('/info/contact_us.html', title='Contact') 