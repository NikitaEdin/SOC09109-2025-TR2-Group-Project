from datetime import datetime
from flask import flash, render_template, request,redirect,url_for
from flask_login import current_user, login_required
from app import app
from app.models import db, Project, checklist_template_optional_checklist,checklist_template_physical,checklist_template_forms_optional,checklist_template_required_rural,checklist_template_required_urban
  
def default_checklist(project_id):
    project = Project.query.get_or_404(project_id)
    
      # Add checklist templates here and in the model if required
    checklist_templates = [
        checklist_template_optional_checklist,
        checklist_template_forms_optional,
        checklist_template_required_rural,
        checklist_template_required_urban,
        checklist_template_physical
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
        
# Add Forms here and their urls to send the user to the form      
def form_url(form_name):
    form_urls ={
        "Viability Study" : "viability_study",
        "Site Evaluation" : "site_evaluation",
        "Loading List" : "loading_list",
        "Post-Flight" : "post_flight"
    }
    return form_urls.get(form_name,"dashboard")

     
        
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
        ),
        "form_url": form_url(item["name"])
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
        ),
        "form_url": form_url(item["name"])
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
        ),
        "form_url": form_url(item["name"])
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

@app.route('/project/<int:project_id>/physical-checklist', methods =['GET','POST'])
@login_required
def physical(project_id):
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
    } for item in checklist_template_physical
}
    content = {
    "checks": checks
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
        
        
        return redirect(url_for('physical', project_id=project.id))
    
    return render_template("checklist/physical_checklist.html",content=content, project=project, footer=False, title='Physical Checklist')