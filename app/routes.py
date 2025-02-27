from app import app
from flask import render_template

from app.models import User, Role, Drone


@app.route('/')
@app.route('/home')
def home():
    drones = Drone.query.limit(3).all()

    return render_template('index.html', title='Home', use_container=False, drones=drones)


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

@app.route("/view-drones")
def view_drones():

    drones = Drone.query.all()

    return render_template('/info/view_drones.html', drones=drones, title='All Drones')


