PostFlightTemplate = [
{
  "title": "Post-Flight Actions",
  "header": "Procedures to follow during landing stage",
  "form": {
    "sections": [
      {
        "header": "During Landing",
        "fields": [
          {"id": "landingpoint", "name": "No crew within 5m of landing point.", "value": "", "type": "checkbox", "required": True},
          {"id": "cleardebris", "name": "TOLZ free of foreign object and debris.", "value": "", "type": "checkbox", "required": True},
          {"id": "seperationdistance", "name": "Uninvolved persons at required separation distance.", "value": "", "type": "checkbox", "required": True},
          {"id": "pilotclear", "name": "Pilot calls Clear.", "value": "", "type": "checkbox", "required": True},
          {"id": "repliesclear", "name": "Designated crew member replies Clear.", "value": "", "type": "checkbox", "required": True},
          {"id": "landsrpa", "name": "Pilot lands RPA.", "value": "", "type": "checkbox", "required": True},
          {"id": "disarmsrpa", "name": "Pilot disarms RPA.", "value": "", "type": "checkbox", "required": True},
          {"id": "powerdownrpa", "name": "Pilot approaches RPA and powers down.", "value": "", "type": "checkbox", "required": True},  
          {"id": "aircraftsafe", "name": "Pilot calls Aircraft safe.", "value": "", "type": "checkbox", "required": True}
        ]
      },
      {
        "header": "After Landing",
        "fields": [
          {"id": "disassembleuas", "name": "Disassemble UAS using model-specific checklist.", "value": "", "type": "checkbox", "required": True},
          {"id": "maintenanceactions", "name": "Record any maintenance actions.", "value": "", "type": "checkbox", "required": True},
          {"id": "recordflight", "name": "Manually record flight data if there is any problem uploading.", "value": "", "type": "checkbox", "required": True},
          {"id": "debriefcrew", "name": "Debrief crew to capture any lessons learned.", "value": "", "type": "checkbox", "required": True},
          {"id": "collectequipment", "name": "Collect and check off any equipment used by the crew.", "value": "", "type": "checkbox", "required": True}
        ]
      },
      {
        "header": "Reporting",
        "fields": [
          {"id": "reportincidents", "name": "Report any incidents.", "value": "", "type": "checkbox", "required": True},
          {"id": "reportairprox", "name": "Report any AIRPROX.", "value": "", "type": "checkbox", "required": True}   
        ]
      }
    ]
  }
}
]
