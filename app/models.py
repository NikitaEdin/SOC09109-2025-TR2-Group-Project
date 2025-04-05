import secrets
from datetime import datetime, timezone
from app import app, db, login_manager, bcrypt
from flask import url_for
from flask_login import UserMixin, current_user
from sqlalchemy import func
import re
# Import the checklist templates
from app.forms.checklist_template import checklist_template_optional_checklist, checklist_template_forms_optional, checklist_template_required_rural, checklist_template_required_urban

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
    flyer_id = db.Column(db.String(20), unique=True, nullable=True)


    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    accessible_projects = db.relationship(
        'Project', secondary='project_access', back_populates='allowed_users'
    )

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

    # Get all logs by user
    def get_all_logs(self):
        return AuditLog.query.filter_by(user_id=self.id).all()
    
    # Get logs by action
    def get_logs_by_action(self, action):
        return AuditLog.query.filter_by(user_id=self.id, action=action).all()


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
    latitude = db.Column(db.Float, nullable=False)

    # Project type
    projectType = db.Column(db.String(50), nullable=False) 

    # Project Purpose
    projectPurposeID = db.Column(db.Integer, db.ForeignKey('project_purpose.id'), nullable=False, default=1)
    projectPurpose = db.relationship('ProjectPurpose', backref='projects')

    # Project details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    dateOfFlight = db.Column(db.Date,  nullable=False)
    
    flightCode = db.Column(db.String(10), nullable=False)
    pilotID = db.Column(db.Integer, nullable=True) # can be linked to User model later
    lastEdited = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # JSON fields
    viabilityStudy = db.Column(db.JSON, nullable=True)
    siteEvaluation = db.Column(db.JSON, nullable=True)
    riskAnalysis = db.Column(db.JSON, nullable=True)
    
    # Loading List Forms 
    crewList = db.Column(db.JSON, nullable=True)
    maintenanceKit = db.Column(db.JSON, nullable=True)
    safetyKit = db.Column(db.JSON, nullable=True)
    equipment = db.Column(db.JSON, nullable=True)
    groundEquipment = db.Column(db.JSON, nullable=True)

    postFlight = db.Column(db.JSON, nullable=True)

    personalChecklist = db.Column(db.JSON, nullable=True)
    toggles = db.Column(db.JSON, nullable=True)


    author = db.relationship('User', backref='projects')

    allowed_users = db.relationship(
        'User', secondary='project_access', back_populates='accessible_projects'
    )

    
    # Returns true if given user is the owner of this project
    def is_owner(self, user):
        return self.authorID == user.id

    # Returns the User obj from the project's author
    def get_author(self):
        return self.author

    def can_access(self):
        return self.authorID == current_user.id or current_user.is_admin() or current_user in self.allowed_users

    def can_edit(self):
        return self.authorID == current_user.id or current_user.is_admin()

    def __repr__(self):
        return f'<Project {self.title} by {self.author.username}>'
    
    # Creates Checklist in the database
    checklist = db.Column(db.JSON, nullable=True)
    
    # Updates the checklist column 
    def update_checklist(self, checklist):
        self.checklist = checklist
        db.session.commit()

    # Get Project purpose
    def get_project_purpose(self):
        return self.projectPurpose
    
    # Set Project Purpose by ID
    def set_project_purpose(self, new_purpose_id):
        purpose = ProjectPurpose.query.get(new_purpose_id)
        if purpose:
            self.projectPurposeID = new_purpose_id
            db.session.commit()
        else:
            raise ValueError("Invalid ProjectPurpose ID")

    # Generate new flightcode based on given project purpose ID
    @staticmethod
    def get_new_flightCode(projectPurposeID):
        purpose = ProjectPurpose.query.get(projectPurposeID)
        if not purpose:
            return "UNKNOWN"

        # Count projects of the same purpose
        count = Project.query.filter_by(projectPurposeID=projectPurposeID).count()
        purpose_code = purpose.code

        # Generate new flight-code
        return f"{purpose_code}{count + 1}"
  

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

    def __repr__(self):
        return f"<AuditLog {self.user_id} - {self.action} at {self.timestamp}>"

###### Drone ######
class Drone(db.Model):
    droneID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    imageURL = db.Column(db.String(255), nullable=False)  
    # Optional information about drone
    weight = db.Column(db.String(50), nullable=True) 
    homePage = db.Column(db.String(255), nullable=True)  
    userGuide = db.Column(db.String(255), nullable=True) 
    best_for = db.Column(db.String(255), nullable=True) 
    release_date = db.Column(db.String(50), nullable=True) 


###### Project Purpose ######
class ProjectPurpose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), nullable=False)
    code = db.Column(db.String(1), nullable=False)

# Association Table for Many-to-Many Relationship
project_access = db.Table(
    'project_access',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(255), nullable=False)  # user-friendly name
    filename = db.Column(db.String(255), nullable=False)  # Unique filename
    filepath = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('files', lazy=True))

    def human_readable_size(self):
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"