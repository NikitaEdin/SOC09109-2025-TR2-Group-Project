# JSON Templates

Documentation to explain the use of JSON in the project.

# Table of Contents

1. [What Features use JSON Templates](#what-features-use-json-templates)
   - [JSON keys](#json-keys)
2. [Examples JSON](#examples-json)
   - [Subsection 2.1](#subsection-21)

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

```json
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


## Things to note

The ```riskAnalysisTemplate.py``` uses Javascript to generate readonly text fields based on the selected hazard these readonly Sections are ```Existing Control```, ```Further Actions```  the javascript works by taking the hazard the user has selected the id associated with it and checks if the ids match for the existing control, further actions, hazards. It does this by removing the prefix from the id for example:
If you pick the hazard ```compliance``` the hidden field will grab the hazards value and then the javascript will grab the value from the hidden field then check if the hidden field value equals any of the further actions & existing controls by appending the value with the prefix of their ids ```_furtheraction``` or ```existing_control``` if the ids match then it shows the existing field and further action related to the hazard.



---



