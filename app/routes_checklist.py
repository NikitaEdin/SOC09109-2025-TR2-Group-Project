from datetime import datetime
from flask import render_template, request,redirect,url_for
from app import app
from app.models import db, Project, checklist_template_optional_checklist,checklist_template_physical,checklist_template_forms_optional,checklist_template_required_rural,checklist_template_required_urban

@app.route("/project/<int:project_id>/rural-checklist", methods=['GET', 'POST'])
def create_project_rural(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Add checklist templates here and in the model if required
    checklist_templates = [
        checklist_template_optional_checklist,
        checklist_template_forms_optional,
        checklist_template_required_rural,
        checklist_template_required_urban
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
        
    if request.method == "POST":
        updated_checklist = []
        
        for item in project.checklist:
            existing_checklist = project.checklist
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            # Grab the status and if it cant put it to false
            existing_status = next((i["status"] for i in existing_checklist if i["name"] == item["name"]), False)
            
            if request.form.get(item["name"]) is None:
                updated_item["status"] = existing_status
            else:
                updated_item["status"] = status
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        # Add any missing items from the checklist template
        project.update_checklist_from_json(updated_checklist)
        
        return redirect(url_for('create_project_rural', project_id=project.id))
    
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
    
    return render_template("create_project/create_project_rural.html", checks=checks, project=project, footer=False)


@app.route("/project/<int:project_id>/urban-checklist", methods=['GET','POST'])
def create_project_urban(project_id):
    
    project = Project.query.get_or_404(project_id)
    
    # Add checklist templates here and in the model if required
    checklist_templates = [
        checklist_template_optional_checklist,
        checklist_template_forms_optional,
        checklist_template_required_rural,
        checklist_template_required_urban
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
        
    if request.method == "POST":
        updated_checklist = []
        
        for item in project.checklist:
            existing_checklist = project.checklist
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            # Grab the status and if it cant put it to false
            existing_status = next((i["status"] for i in existing_checklist if i["name"] == item["name"]), False)
            
            if request.form.get(item["name"]) is None:
                updated_item["status"] = existing_status
            else:
                updated_item["status"] = status
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        # Add any missing items from the checklist template
        project.update_checklist_from_json(updated_checklist)
        
        return redirect(url_for('create_project_urban', project_id=project.id))
    
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
    
    return render_template("create_project/create_project_urban.html", checks=checks, project=project, footer=False)

@app.route('/project/<int:project_id>/optional-checklist', methods =['GET','POST'])
def optional(project_id):
    
    project = Project.query.get_or_404(project_id)
    
    checklist_templates=[
        checklist_template_optional_checklist,
        checklist_template_forms_optional,
        checklist_template_required_rural,
        checklist_template_required_urban
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
            existing_checklist = project.checklist
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            # Grab the status and if it cant put it to false
            existing_status = next((i["status"] for i in existing_checklist if i["name"] == item["name"]), False)
            
            if request.form.get(item["name"]) is None:
                updated_item["status"] = existing_status
            else:
                updated_item["status"] = status
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        # Add any missing items from the checklist template
        project.update_checklist_from_json(updated_checklist)
        
        return redirect(url_for('optional', project_id=project.id))

#  This is to tidy up and only pass in only one variable into the template
    content = {
    "checks": checks,
    "forms": forms
}
    return render_template("create_project/optional_forms.html", content=content, project=project,footer=False )

@app.route('/project/<int:project_id>/physical-checklist', methods =['GET','POST'])
def physical(project_id):
    project = Project.query.get_or_404(project_id)
    
    checklist_templates=[
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
            existing_checklist = project.checklist
            status = request.form.get(item["name"]) == "on"
            
            updated_item = item.copy()
            
            # Grab the status and if it cant put it to false
            existing_status = next((i["status"] for i in existing_checklist if i["name"] == item["name"]), False)
            
            if request.form.get(item["name"]) is None:
                updated_item["status"] = existing_status
            else:
                updated_item["status"] = status
                
            # Update only if the status changed
            if updated_item["status"] != item["status"]:
                updated_item["last_edit"] = datetime.now().strftime("%d/%m/%y %H:%M")
            
            updated_checklist.append(updated_item)

        # Update the project checklist
        project.update_checklist(updated_checklist)
        
        # Add any missing items from the checklist template
        project.update_checklist_from_json(updated_checklist)
        
        return redirect(url_for('physical', project_id=project.id))
    
    return render_template("checklist/physical_checklist.html",content=content, project=project,footer=False )