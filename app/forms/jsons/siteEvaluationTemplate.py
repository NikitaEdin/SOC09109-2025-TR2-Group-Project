SiteEvaluationTemplate = [
{
  "title": "Site Evaluation Study",
  "header": "Site evaluation form",
  "form": {
    "sections": [
      {
        "header": "Flight Details",
        "fields": [
          {"id": "flightcode", "name": "Flight Code", "value": "", "type": "text", "required": True},
          {"id": "dateofflight", "name": "Date of Flight", "value": "", "type": "date", "required": True},
          {"id": "remotepilot", "name": "Remote Pilot", "value": "", "type": "text", "required": True},
          {"id": "datecompleted", "name": "Date Completed", "value": "", "type": "date", "required": True},
        ]
      },

      {
          "header": "Pre-site Visit",
          "fields": [
              {"id": "locationdescription", "name":"Location Description", "value": "", "type": "textarea"},
              {"id": "sensitivies", "name": "Sensetivies", "value": "", "type": "textarea"},
              {"id": "airspace", "name":"Airspace", "value": "", "type": "textarea"},
              {"id": "restrictions", "name":"Restrictions", "value": "", "type": "textarea"},
              {"id": "terrian", "name":"Terrian", "value": "", "type": "textarea"},
              {"id": "aviationproximities", "name":"Aviation Proximities", "value": "", "type": "textarea"},
              {"id": "permissions", "name":"Permissions", "value": "", "type": "textarea"},
              {"id": "notams", "name":"NOTAMS", "value": "", "type": "textarea"},
              {"id": "PPE", "name":"PPE Requirements", "value": "", "type": "textarea"},
              {"id": "livestock", "name":"Livestock", "value": "", "type": "textarea"},
              {"id": "people", "name":"People", "value": "", "type": "textarea"},
              {"id": "hazards", "name":"Hazards", "value": "", "type": "textarea"},
              {"id": "footpaths", "name":"Footpaths", "value": "", "type": "textarea"},
              {"id": "vehicleaccess", "name":"Vehicle Access", "value": "", "type": "textarea"},
              {"id": "signalcoverage", "name":"Mobile Phone Coverage", "value": "", "type": "textarea"}
          ]
      },

      {
          "header": "Emergency Contact Details",
          "fields": [
              {"id": "localpolice", "name":"Local Police", "value": "", "type": "textarea"},
              {"id": "localatc", "name":"Local ATC", "value": "", "type": "textarea"},
              {"id": "military", "name":"Military Low flying booking cell", "value": "", "type": "textarea"},
              {"id": "hospital", "name":"Local Hospitcal", "value": "", "type": "textarea"}
          ]
      },

      {
          "header": "Airspace and Environment Diagrams",
          "fields": [
              {"id": "airspacenotes", "name":"Airspace Notes", "value": "", "type": "textarea"},
              {"id": "environmentnotes", "name":"Environment Notes", "value": "", "type": "textarea"},
          ]
      },

      {
          "header": "Site Survey",
          "fields": [
              {"id": "presitevisit", "name":"Pre-site Visit Date", "value": "", "type": "date"},
              {"id": "obstructions2", "name":"Obstructions", "value": "", "type": "textarea"},
              {"id": "people2", "name":"People", "value": "", "type": "textarea"},
              {"id": "livestock2", "name":"Livestock", "value": "", "type": "textarea"},
              {"id": "proximity2", "name":"Proximity", "value": "", "type": "textarea"},
              {"id": "primarytolz", "name":"Primary TOLZ", "value": "", "type": "textarea"},
              {"id": "secondarytolz", "name":"Secondary TOLZ", "value": "", "type": "textarea"},
              {"id": "comms2", "name":"Comms", "value": "", "type": "textarea"},
              {"id": "Other", "name":"other", "value": "", "type": "textarea"},
          ]
      }
    ]
  }
}
]
