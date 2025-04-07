PostFlightTemplate = [
{
  "title": "Post-Flight Actions",
  "header": "Procedures to follow during landing stage",
  "form": {
    "sections": [
      {
        "header": "During Landing",
        "fields": [
          {"id": "landingpoint", "name": "No crew within 5m of landing point.", "value": "", "type": "checkbox"},
          {"id": "cleardebris", "name": "TOLZ free of foreign object and debris.", "value": "", "type": "checkbox"},
          {"id": "seperationdistance", "name": "Uninvolved persons at required separation distance.", "value": "", "type": "checkbox"},
          {"id": "pilotclear", "name": "Pilot calls Clear.", "value": "", "type": "checkbox"},
          {"id": "repliesclear", "name": "Designated crew member replies Clear.", "value": "", "type": "checkbox"},
          {"id": "landsrpa", "name": "Pilot lands RPA.", "value": "", "type": "checkbox"},
          {"id": "disarmsrpa", "name": "Pilot disarms RPA.", "value": "", "type": "checkbox"},
          {"id": "powerdownrpa", "name": "Pilot approaches RPA and powers down.", "value": "", "type": "checkbox"},  
          {"id": "aircraftsafe", "name": "Pilot calls Aircraft safe.", "value": "", "type": "checkbox"}
        ]
      },
      {
        "header": "After Landing",
        "fields": [
          {"id": "disassembleuas", "name": "Disassemble UAS using model-specific checklist.", "value": "", "type": "checkbox"},
          {"id": "maintenanceactions", "name": "Record any maintenance actions.", "value": "", "type": "checkbox"},
          {"id": "recordflight", "name": "Manually record flight data if there is any problem uploading.", "value": "", "type": "checkbox"},
          {"id": "debriefcrew", "name": "Debrief crew to capture any lessons learned.", "value": "", "type": "checkbox"},
          {"id": "collectequipment", "name": "Collect and check off any equipment used by the crew.", "value": "", "type": "checkbox"}
        ]
      },
      {
        "header": "Reporting",
        "fields": [
          {"id": "reportincidents", "name": "Report any incidents.", "value": "", "type": "checkbox"},
          {"id": "reportairprox", "name": "Report any AIRPROX.", "value": "", "type": "checkbox"}   
        ]
      }
    ]
  }
}
]
