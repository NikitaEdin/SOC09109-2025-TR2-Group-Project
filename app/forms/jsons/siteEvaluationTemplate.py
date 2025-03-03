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
              {"id": "sensitivies", "name": "Sensetivies", "value": "", "type": "textarea",
               "description": "This could include schools, cemeteries, government buildings where flying a drone in the vicinity.",
               "tooltip": "This may help you to decide if it would be worth informing the police via 101."},
              {"id": "airspace", "name":"Airspace", "value": "", "type": "textarea",
               "description": "Example 1: No ATC Permission required Class G airspace uncontrolled<br>Example 2: No ATC Permission required, ATC Notification if deemed necessary Class D airspace Leeds Bradford CTR – Surface – 4500ft amsl<br>Example 3 – ATC Permission required Leeds Bradford Flight restriction zone "},
              {"id": "restrictions", "name":"Restrictions", "value": "", "type": "textarea",
               "description": "This is specifically looking at restricted, danger and prohibited airspace",
               "tooltip": "This will be useful to identify and additional permission needed if looking to operate within."},
              {"id": "terrian", "name":"Terrian", "value": "", "type": "textarea",
               "description": "This will be useful to identify and additional permission needed if looking to operate within."},
              {"id": "aviationproximities", "name":"Aviation Proximities", "value": "", "type": "textarea",
               "description": "What is the distance and direction to places where people non under your control could be found?",
               "tooltip": "This would be a brief overview of any other airspace proximities"},
              {"id": "permissions", "name":"Permissions", "value": "", "type": "textarea",
               "description": "Do you have permission to operate from that location you should be aware of any issues around byelaws and trespass. "},
              {"id": "notams", "name":"NOTAMS", "value": "", "type": "textarea",
               "description": "Are there any temporary restricted areas or temporary danger areas identified by NOTAM?"},
              {"id": "PPE", "name":"PPE Requirements", "value": "", "type": "textarea",
               "description": "Your/client minimum PPE requirements in line with OM"},
              {"id": "livestock", "name":"Livestock", "value": "", "type": "textarea",
               "description": "Is there a potential for livestock, birds etc at the purposed flight location?"},
              {"id": "people", "name":"People", "value": "", "type": "textarea",
               "description": "What is the distance and direction to places where people non under your control could be found?"},
              {"id": "hazards", "name":"Hazards", "value": "", "type": "textarea",
               "tooltip": "e.g. Transmitters, Power Pylons etc"},
              {"id": "footpaths", "name":"Footpaths", "value": "", "type": "textarea"},
              {"id": "vehicleaccess", "name":"Vehicle Access", "value": "", "type": "textarea",
               "description": "1 – where is the parking for the pilot<br>2 – can members of the public access the flight area by vehicles"},
              {"id": "signalcoverage", "name":"Mobile Phone Coverage", "value": "", "type": "textarea"}
          ]
      },

      {
          "header": "Emergency Contact Details",
          "fields": [
              {"id": "localpolice", "name":"Local Police", "value": "", "type": "textarea",
               "description": "If you were to log a flight via 101 this is where you could write down the case number for reference if needed"},
              {"id": "localatc", "name":"Local ATC", "value": "", "type": "textarea",
               "description": "Direct line to ATC is what you will want to obtain if possible.",
               "tooltip": "This is obtained via the NATS AIS Website > EAIP link > Part 3 > AD2"},
              {"id": "military", "name":"Military Low flying booking cell", "value": "", "type": "textarea",
               "description": "0800 515544"},
              {"id": "hospital", "name":"Local Hospitcal", "value": "", "type": "textarea",
               "description": "Local A&E include address/ postcode could be useful to obtain and have to hand in the event of incident or accident if unfamiliar with the location."}
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
              {"id": "obstructions2", "name":"Obstructions", "value": "", "type": "textarea",
               "description": "Any changes that might need to be considered within the planned flight or updated within the risk assessment",
               "tooltip": "Masts, Wires, Buildings, Train lines, Trees, Lakes, Rivers etc."},
              {"id": "people2", "name":"People", "value": "", "type": "textarea",
               "tooltip": "Cordon requirement, Crowd Control.", "description": "Any changes that might need to be considered within the planned flight or updated within the risk assessment"},
              {"id": "livestock2", "name":"Livestock", "value": "", "type": "textarea",
               "tooltip": "Farm animals, Dogs, Wildlife.", "description": "Any changes that might need to be considered within the planned flight or updated within the risk assessment"},
              {"id": "proximity2", "name":"Proximity", "value": "", "type": "textarea",
               "tooltip": "Public, Road Users.", "description": "Any changes that might need to be considered within the planned flight or updated within the risk assessment"},
              {"id": "primarytolz", "name":"Primary TOLZ", "value": "", "type": "textarea",
               "description": "Needs to comply with applicable legislation around separation distances."},
              {"id": "secondarytolz", "name":"Secondary TOLZ", "value": "", "type": "textarea",
               "description": "Needs to comply with applicable legislation around separation distances."},
              {"id": "comms2", "name":"Comms", "value": "", "type": "textarea",
               "tooltip": "Communications required by ops team"},
              {"id": "Other", "name":"other", "value": "", "type": "textarea",
               "description": "Any other factors that might affect the safety of the flight"},
          ]
      }
    ]
  }
}
]
