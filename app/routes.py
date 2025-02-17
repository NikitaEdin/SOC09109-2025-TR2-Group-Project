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

@app.route("/view-drones")
def view_drones():

    drones = {
        '1': {
            'name': 'DJI Matrice 350 RTK',
            'image_path': 'Images/Matrice350RTK.jpg'
        },
        '2': {
            'name': 'DJI Mavic 3E',
            'image_path': '/Images/coenkpz4.png'
        },
        '3': {
            'name': 'DJI Mini 3 Pro',
            'image_path': '/Images/Mini3Pro.jpeg'
        }
    }

    """
        '4': {
            'name': 'Drone 4',
            'image_path': '/Images/DroneCityEdited.jpg'
        },
        '5': {
            'name': 'Drone 5',
            'image_path': '/Images/DroneCityEdited.jpg'
        },
        '6': {
            'name': 'Drone 6',
            'image_path': '/Images/DroneCityEdited.jpg'
        },
        '7': {
            'name': 'Drone 7',
            'image_path': '/Images/DroneCityEdited.jpg'
        }
    """

    return render_template('/info/view_drones.html', drones=drones)


