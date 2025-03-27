riskAnalysisTemplate = [
{
  "title": "Risk Analysis Form",
  "header": "Risks and hazards related to the project",
  "form": {
    "sections": [
      {
        "header": "Hazards Identified",
        "dropdown_hazards": [
          {"id": "compliance", "name": "Compliance", "value":"","required": True},
          {"id": "competence", "name": "Competence", "value":"","required": True},
          {"id": "permission", "name": "Permission", "value":"","required": True},
          {"id": "weather", "name": "Weather","value":"","required": True},
          {"id": "pederstrians_traffic", "name": "Pedestrians and Traffic","value":"","required": True},
          {"id": "emergency", "name": "Emergency","value":"","required": True},
          {"id": "wildlife_pets", "name": "Wildlife, Livestock, Domestic pets etc","value":"","required": True},
          {"id": "collision_nearmiss", "name": "UAS collision or near miss with other air users","value":"","required": True},
          {"id": "maintenance_servicing", "name": "Maintenance and servicing","value":"","required": True},
          {"id": "crash_building", "name": "Crash into building/people","value":"","required": True},
          {"id": "security", "name": "Security","value":"","required": True},
          {"id": "insurance", "name": "Insurance","value":"","required": True},
          {"id": "data_protection", "name": "Data Protection/camera","value":"","required": True},
          {"id": "ground_hazards", "name": "Ground Hazards","value":"","required": True},
          {"id": "other_hazards", "name": "Any other Hazards/risks","value":"","required": True},
        ]
      },
      {
        "header": "Existing Control",
        "existing_control":[
          {"id": "compliance_control", "name": 
            """All drones/UAVs registered.\n The remote pilot must not fly the aircraft in any of the circumstances described below except in accordance with a permission issued by the CAA.\n Dont fly near airports or airfields without permission from air traffic control, Observe your drone/UAV at all times  stay 150ft (50m) away from people and property.\n Drones/UAVs with surveillance cameras must not be flown within 50 metres of any person unless approval has been permitted, Comply with Operation Manual."""},
          
          {"id": "competence_control", "name":
            """All drone remote pilots need to be registered with the CAA and all drones/UAVs need to have the registration number attached."""},
          
          {"id": "permission_control", "name":
            """The pilot will seek permission in advance in line with the University procedure.\n Off campus, permission to fly is required from the property owner.\n Where required notification to air traffic control.\n Approval of location and risk assessment to area must be completed."""},
          
          {"id": "weather_control", "name":
            """Accurate weather forecast checked prior to flight.\n Weather to be monitored at all times during flight with a view to landing should weather deteriorate."""},
           
          {"id": "pederstrians_traffic_control", "name":
            """Tape off exclusion zone where possible.\n At least one spotter is dedicated to supervising access to zone.\n Flying in the middle of the field and away from pedestrians and traffic."""},
           
          {"id": "emergency_control", "name":
            """Local emergency arrangements in place.\n Campus induction leaflet communicated."""},
           
          {"id": "wildlife_pets_control", "name":
            """Risk assess area prior to flight of risks to livestock or restrictions.\n Keep a responsible distance away from domestic animals, pets and working animals (e.g. assistance dogs)."""},
           
          {"id": "collision_nearmiss_control", "name":
            """Activity in line with CAA legislative requirements and Operations Manual.\n Air Traffic Control will be informed. """},
           
          {"id": "maintenance_servicing_control", "name":
            """The drone/UAV will be serviced and maintained in line with the manufacturers instructions.\n Batteries will be stored within a fireproof bag whilst they are charging. """},
           
          {"id": "crash_building_control", "name":
            """The remote pilot has undertaken relevant training.\n The Pilot must ensure they are 50 meters away from people and property."""},
           
          {"id": "security_control", "name":
            """No lone working when flying drone/UAV permitted.\n Staff will not leave any property unattended."""},
           
          {"id": "insurance_control", "name":
            """The Universitys public liability and employers liability insurances would respond where damage and/or injury to 3rd party property, assets or individuals was caused by flight of a drone/UAV and the University was found to be negligent.\n Insurance stipulates NQE training required."""},
          
          {"id": "data_protection_control", "name":
            """Consideration must be given in relation to images gathered.\n This must be taken into account when considering the flight location and should be stated in the site-specific risk assessment if applicable."""},
          
          {"id": "ground_hazards_control", "name":
            """e.g. Trees, unstable terrain, buildings, water, etc."""},
          
          {"id": "other_hazards_control", "name":
            """Anything not listed."""},
          
        ]
      },
      {
        "header": "People at Risk",
        "dropdown_people":[
            {"id": "all", "name": "All in vicinity","value":"","required": True},
            {"id": "staff", "name": "Staff in vicinity","value":"","required": True},
            {"id": "students", "name": "Students in vicinity","value":"","required": True},
            {"id": "visitors", "name": "Visitors in vicinity","value":"","required": True},
            {"id": "pedestrians", "name": "Pedestrians","value":"","required": True},
        ]
      },
      {
        "header": "Risk"
      },
      {
        "header": "Further Actions"
      },
      {
        "header": "Residual Risk"
      },
      {
        "header": "Action Taken By"
      },
      {
        "header": "Action Taken When"
      },
      {
        "header": "Completed"
      }
    ]
  }
}
]
