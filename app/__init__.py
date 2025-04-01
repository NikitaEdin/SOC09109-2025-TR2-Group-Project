import os
from flask import Blueprint, Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

# Secret key loaded from env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Session set to timeout after 5 minutes
# logs out user for inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# resets inactivity timer on each request made
@app.before_request
def before_request():
    session.permanent = True
    session.modified = True
    
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Password Encryption
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Import routes
from app import routes
from app import routes_auth
from app import routes_wizard
from app import routes_forms
from app import routes_dashboard
from app import routes_new_project
from app import routes_checklist
from app import routes_settings
from app import routes_errors

routes_errors.error_handlers(app)
