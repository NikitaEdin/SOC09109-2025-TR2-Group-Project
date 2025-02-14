import secrets
from datetime import datetime, timezone
from app import app, db, login_manager, bcrypt
from flask import url_for
from flask_login import UserMixin, current_user
from sqlalchemy import func
import re

# Global/static variables
ADMIN_MIN_POWER = 90


###### USER ######
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    displayname = db.Column(db.String(20))

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    # ToString
    def __repr__(self):
        return f"<User {self.username} ({self.role.title})>"

    # Has the password
    def set_password(self, password):
         self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check the hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    # Return true if user has enough power for admin role
    def is_admin(self):
        return self.role.power >= ADMIN_MIN_POWER
    
    # Get all projects by this user
    def get_projects(self):
        return Project.query.filter_by(authorID=self.id).all()


###### ROLES ######

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    power = db.Column(db.Integer, nullable=False, default=0)

    # ToString
    def __repr__(self):
        return f"<Role {self.title} (Power: {self.power})>"
    
    # Check if this user has more power than the given user
    def has_higher_power_than(self, other_role):
        return self.power > other_role.power
    

###### Project ######
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Location
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=False)

    # Project type
    projectType = db.Column(db.String(50), nullable=False) 

    # Project details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    dateOfFlight = db.Column(db.Date,  nullable=False)
    
    flightCode = db.Column(db.String(50), nullable=True ) # nullable for now.
    pilotID = db.Column(db.Integer, nullable=True) # can be linked to User model later
    lastEdited = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # JSON fields
    viabilityStudy = db.Column(db.JSON, nullable=True)
    siteEvaluation = db.Column(db.JSON, nullable=True)
    riskAnalysis = db.Column(db.JSON, nullable=True)
    loadingList = db.Column(db.JSON, nullable=True)
    postFlight = db.Column(db.JSON, nullable=True)

    # Returns true if given user is the owner of this project
    def is_owner(self, user):
        return self.authorID == user.id

    def __repr__(self):
        return f'<Project {self.title} by {self.author.username}>'