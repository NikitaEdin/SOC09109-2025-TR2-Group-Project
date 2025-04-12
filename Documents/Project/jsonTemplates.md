# JSON Templates

Documentation to explain the use of JSON in the project.

# Table of Contents

1. [What Features use JSON Templates](#what-features-use-json-templates)
   - [JSON keys](#json-keys)
2. [Examples JSON](#examples-json)
   - [Checkbox inputs](#checkbox-inputs)
   - [Text, Date, Textarea inputs](#text-date-textarea-inputs)
   - [Url Inputs](#url-input)
3. [Creating new templates](#create-new-templates)
    - [What to do](#what-to-do)
4. [Things to Note](#things-to-note)


## What Features use JSON Templates
- Loading List: Equipment, Group Equipment, Crew List, Maintenance Kit, Safety Kit 
- Checklists: Rural Checklist, Urban Checklist
- Required Forms: Risk Analysis, Site Evaluation, Viability Study
- Pre flight form & Post flight form
- Static Timeline

### JSON keys 

- "header" key in the json controls the header.
- "fields" key is a dictionary that holds all the fields.
- "id" key is the id that is used for the input id.
- "name" key is used for the name of the input which gets used in the front-end.
- "value" key is used for the form to store the value of the form based on user input. 
- "type" key is to determine the type of form input so for example "checkbox", "text", "date", "textarea". 
- "required" key is used in the form to determine if its required or not.
- "description" key is used to describe a form input which is used in the checkbox templates.

## Examples JSON
### Checkbox inputs

``` json
LoadingListMaintenanceKitTemplate = [
{
  "title": "Loading List - Maintenance Kit",
  "header": "Ensure all maintenance kit items are checked before proceeding.",
  "form": {
    "sections": [
      {
        "header": "Maintenance Equipment",
        "fields": [
          {"id": "props", "name": "Spare props", "value": "", "type": "checkbox", "required": False},
          {"id": "cables", "name": "Spare cables", "value": "", "type": "checkbox", "required": False},
          {"id": "allenkeys", "name": "Allen keys", "value": "", "type": "checkbox", "required": False},
          {"id": "screwdrivers", "name": "Screwdrivers", "value": "", "type": "checkbox", "required": False},
          {"id": "calibration", "name": "Calibration platform", "value": "", "type": "checkbox", "required": False}
        ]
      }
    ]
  }
}
]
```
#### Form using the JSON template above
![alt text](images/checkbox.png)
### Text, Date, Textarea inputs

``` json
ViabilityStudyTemplate = [
{
  "title": "Viability Study",
  "header": "Analysing risks, requirements, and operational feasibility",
  "form": {
    "sections": [
      {
        "header": "Flight Information",
        "fields": [
          {"id": "flightcode", "name": "Flight Code", "value": "", "type": "text", "required": True},
          {"id": "description", "name": "Description", "value": "", "type": "textarea", "required": True},
          {"id": "flightdate", "name": "Flight Date", "value": "", "type": "date", "required": True},
          {"id": "allowedUsers", "name": "Project Members", "type": "div"}
        ]
      }
```
#### Form using the JSON template above
![alt text](images/text-date.png)

### Url input
``` json
Timeline_data = [
{
  "sections": [
    {
      "title": "28 Days in Advance",
      "items": [
        {
          "text": "Apply for non-standard flight permission if required",
          "url": "https://nsf.nats.aero/drones-and-model-aircraft/"
        }
      ]
    }

```
#### Form using the JSON template above
![alt text](images/url.png)

## Create new templates
### What to do
#### First Step - Create JSON Template
1. Create the a JSON template in the directory ```\app\forms\jsons```
2. Use the one of the structures that fits your need text, checkbox etc.

#### Second Step - Load JSON into the Database
1. In the root of the project folder go to ```routes_new_project.py```
2. Import the template you just created ```from app.forms.jsons.TemplateFileName import JSON```
3. Scroll to the project initation for the jsons it should look like this:
``` python  
# JSON forms
  viabilityStudy = viability_study_value,
  siteEvaluation = site_evaluation_value,
  riskAnalysis = riskAnalysisTemplate[0],
  toggles = togglesJSON,
```
4. Add the JSON template to the project ```formName = TemplateName[0]```
5. Navigate to the root of the project to a file called ```models.py``` scroll down to the creating the table project and add your form to the project table for example: 
``` python 
# JSON fields
    viabilityStudy = db.Column(db.JSON, nullable=True)
    siteEvaluation = db.Column(db.JSON, nullable=True)
    riskAnalysis = db.Column(db.JSON, nullable=True)
```
#### Third Step - Backend
1. Navigate to the file ```routes_forms.py``` in the project root
2. Create a route for the form that you are going to create it could look like something like this:
``` python
# Loading List EQUIPMENT KIT Form Route (JSON GENERATION)
@app.route("/project/<int:project_id>/loading-list/equipment", methods=["GET", "POST"])
@login_required
def loading_list_equipment(project_id):
    project = Project.query.get_or_404(project_id)  
    security(project)
    
    form_data = project.equipment    
    errors = {}  # validation errors
    
    if request.method == 'POST':
        # Loop through each section
        for section in form_data[0]['form']['sections']:
            # Loop through all fields
            for field in section['fields']:
                field_id = field['id']  
               
                # Handle checkboxes 
                if field['type'] == 'checkbox':  
                    field['value'] = request.form.get(field_id) == "on"  # True if checked
                else:
                    field['value'] = False

        # Any errors? don't commit the changes
        if errors:
            return render_template('/forms/loading/equipment_json.html', project=project, form_data=form_data, errors=errors)

        # Save changes
        project.equipment = form_data
        flag_modified(project, "equipment")
        db.session.add(project)
        db.session.commit()

        flash('Changes saved successfully!', 'success')
    
    return render_template("/forms/loading/equipment_json.html", project=project, form_data=form_data, footer=False, title="Equipment" )
```           

## Things to note
> [!NOTE]
>  The ```riskAnalysisTemplate.py``` uses Javascript to generate readonly text fields based on the selected hazard these readonly Sections are ```Existing Control```, ```Further Actions```. The javascript works by taking the hazard the user has selected the id associated with it and checks if the ids match for the existing control, further actions, hazards. It does this by removing the prefix from the id for example:
If you pick the hazard ```compliance``` the hidden field will grab the hazards value and then the javascript will grab the value from the hidden field then check if the hidden field value equals any of the further actions & existing controls by appending the value with the prefix of their ids ```_furtheraction``` or ```_control``` if the ids match then it shows the existing field and further action related to the hazard.








