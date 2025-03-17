from datetime import datetime
from flask import flash, render_template, request,redirect,url_for
from flask_login import current_user, login_required
from app import app
from app.models import db, Project, checklist_template_optional_checklist,checklist_template_forms_optional,checklist_template_required_rural,checklist_template_required_urban
from sqlalchemy.orm.attributes import flag_modified


def default_checklist(project_id):
    project = Project.query.get_or_404(project_id)
    
      # Add checklist templates here and in the model if required
    checklist_templates = [
        checklist_template_optional_checklist,
        checklist_template_forms_optional,
        checklist_template_required_rural,
        checklist_template_required_urban,
        
    ]
    
    # Checks if the checklist templates is generated if not give it default values
    if not project.checklist:
        project.checklist = []
        
        for template in checklist_templates:
            for item in template:
                project.checklist.append({
                    "name": item["name"],
                    "status": False,
                    "last_edit": None
                })
        db.session.commit()
     
        
@app.route("/project/<int:project_id>/rural-checklist", methods=['GET', 'POST'])
@login_required
def rural_checklist(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Restrict access to only rural project types
    if project.projectType != 'Rural':
        flash("Project is not of type Rural.", 'danger')
        return redirect(url_for('project', project_id = project.id))
    
    # Ensure project is owned by current_user or user is an admin
    if not project.can_access():
        flash("You are not authorised to access this project.", "danger")
        return redirect(url_for('dashboard'))
     

    default_checklist(project_id)
        
    if request.method == "POST":
        updated_checklist = []
        
        for item in project.checklist:
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            
            if item["name"] in request.form:
                updated_item["status"] = status
            else: 
                updated_item["status"] = item["status"]
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)
            
        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        return redirect(url_for('rural_checklist', project_id=project.id))
    
    checks={
        item["name"]: {
        "title": item["name"],
        "description": item["description"],
     "value": next(
            (check["status"] for check in project.checklist if check["name"] == item["name"]), 
            False  # Default to False if no match is found
        ),
        "last_edit": next(
            (check["last_edit"] for check in project.checklist if check["name"] == item["name"]),
            None  # Default to None if no match is found
        )
    } for item in checklist_template_required_rural
}
    
    return render_template("checklist/rural_checklist.html", checks=checks, project=project, footer=False, title='Required Forms')


@app.route("/project/<int:project_id>/urban-checklist", methods=['GET','POST'])
@login_required
def urban_checklist(project_id):
    project = Project.query.get_or_404(project_id)

    # Restrict access to only rural project types
    if project.projectType != 'Urban':
        flash("Project is not of type Urban.", 'danger')
        return redirect(url_for('project', project_id = project.id))
    
     # Ensure project is owned by current_user or user is an admin
    if not project.can_access():
        flash("You are not authorised to access this project.", "danger")
        return redirect(url_for('dashboard'))
    
    default_checklist(project_id)
        
    if request.method == "POST":
        updated_checklist = []
        
        for item in project.checklist:
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            if item["name"] in request.form:
                updated_item["status"] = status
            else: 
                updated_item["status"] = item["status"]
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        
        return redirect(url_for('urban_checklist', project_id=project.id))
    
    checks={
        item["name"]: {
        "title": item["name"],
        "description": item["description"],
        "value": next(
            (check["status"] for check in project.checklist if check["name"] == item["name"]), 
            False  # Default to False if no match is found
        ),
        "last_edit": next(
            (check["last_edit"] for check in project.checklist if check["name"] == item["name"]),
            None  # Default to None if no match is found
        )
    } for item in checklist_template_required_urban
}
    
    return render_template("checklist/urban_checklist.html", checks=checks, project=project, footer=False, title='Required Forms')

@app.route('/project/<int:project_id>/optional-checklist', methods =['GET','POST'])
@login_required
def optional(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Ensure project is owned by current_user or user is an admin
    if not project.can_access():
        flash("You are not authorised to access this project.", "danger")
        return redirect(url_for('dashboard'))

    default_checklist(project_id)
           
    # Stores information from the checklist template
    checks={
        item["name"]: {
        "title": item["name"],
        "description": item["description"],
         "value": next(
            (check["status"] for check in project.checklist if check["name"] == item["name"]), 
            False  # Default to False if no match is found
        ),
        "last_edit": next(
            (check["last_edit"] for check in project.checklist if check["name"] == item["name"]),
            None  # Default to None if no match is found
        )
    } for item in checklist_template_optional_checklist
}
     
    forms={
        item["name"]: {
        "title": item["name"],
        "description": item["description"],
        "value": next(
            (check["status"] for check in project.checklist if check["name"] == item["name"]), 
            False  # Default to False if no match is found
        ),
        "last_edit": next(
            (check["last_edit"] for check in project.checklist if check["name"] == item["name"]),
            None  # Default to None if no match is found
        )
    } for item in checklist_template_forms_optional
    }
    
    # On form submission checks if the checkbox is marked  then puts it into updated checklist
    if request.method == "POST":
        updated_checklist = []
        
        for item in project.checklist:
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            
            if item["name"] in request.form:
                updated_item["status"] = status
            else: 
                updated_item["status"] = item["status"]
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)
            

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        return redirect(url_for('optional', project_id=project.id))

#  This is to tidy up and only pass in only one variable into the template
    content = {
    "checks": checks,
    "forms": forms
}
    return render_template("checklist/optional_checklist.html", content=content, project=project, footer=False, title='Optional Forms')


# Personal Checklist Route
@app.route('/project/<int:project_id>/personal-checklist', methods=['GET', 'POST'])
@login_required
def personal(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Message for project authorisation
    if not project.can_access():
        flash("You are not authorised to access this project.", "danger")
        return redirect(url_for('dashboard'))
    
    # Initialise empty checklist if doesn't already exist
    if not hasattr(project, 'personalChecklist') or not project.personalChecklist:
        project.personalChecklist = []
        flag_modified(project, "personalChecklist")
        db.session.add(project)
        db.session.commit()
    
    if request.method == "POST":
        updated_checklist = []
        
        # Get the action items from the form
        actions = request.form.getlist('action[]')
        checks = request.form.getlist('check[]')
        
        # Create updated checklist from form
        for i, action in enumerate(actions):
            if action.strip():
                # Determine if checked
                is_checked = str(i) in checks
                
                # Find the item in the original checklist
                original_item = None
                for item in project.personalChecklist:
                    if item["name"] == action:
                        original_item = item
                        break
                
                # Create new item
                new_item = {
                    "id": str(i),
                    "name": action,
                    "status": is_checked,
                }
                
                # Update timestamp only if status changed
                if original_item:
                    # If the item was created before, copy its timestamp
                    new_item["last_edit"] = original_item.get("last_edit")
                    
                    # Update timestamp only if status changed
                    if original_item["status"] != is_checked:
                        new_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
                else:
                    # Set timestamp for new item
                    new_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
                
                updated_checklist.append(new_item)
        
        # Update the project's personal checklist
        project.personalChecklist = updated_checklist
        flag_modified(project, "personalChecklist")
        db.session.add(project)
        db.session.commit()
        
        flash("Changes saved successfully.", "success")
        return redirect(url_for('project', project_id=project.id))
    
    return render_template("checklist/personal_checklist.html", project=project, footer=False, title='Personal Checklist')