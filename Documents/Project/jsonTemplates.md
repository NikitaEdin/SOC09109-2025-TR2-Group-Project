# JSON Templates

Documentation to explain the use of JSON in the project.

# Table of Contents

1. [What Features use JSON Templates](#what-features-use-json-templates)
   - [JSON keys](#json-keys)
2. [Examples JSON](#examples-json)
   - [Checkbox inputs](#checkbox-inputs)
   - [Text, Date, Textarea inputs](#text-date-textarea-inputs)
   - [Url Inputs](#url-input)
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


## Things to note
> [!NOTE]
>  The ```riskAnalysisTemplate.py``` uses Javascript to generate readonly text fields based on the selected hazard these readonly Sections are ```Existing Control```, ```Further Actions```. The javascript works by taking the hazard the user has selected the id associated with it and checks if the ids match for the existing control, further actions, hazards. It does this by removing the prefix from the id for example:
If you pick the hazard ```compliance``` the hidden field will grab the hazards value and then the javascript will grab the value from the hidden field then check if the hidden field value equals any of the further actions & existing controls by appending the value with the prefix of their ids ```_furtheraction``` or ```_control``` if the ids match then it shows the existing field and further action related to the hazard.








