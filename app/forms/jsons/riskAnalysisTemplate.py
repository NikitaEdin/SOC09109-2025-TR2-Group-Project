riskAnalysisTemplate = [
{
  "title": "Risk Analysis Form",
  "header": "Risks and hazards related to the project",
  "form": {
    "sections": [
      {
        "header": "Hazards Identified",
        "dropdown_hazards": [
          {"id": "compliance", "name": "Compliance","required": True},
          
          {"id": "competence", "name": "Competence","required": True},
          
          {"id": "permission", "name": "Permission","required": True},
          
          {"id": "weather", "name": "Weather","required": True},
          
          {"id": "pederstrians_traffic", "name": "Pedestrians and Traffic","required": True},
          
          {"id": "emergency", "name": "Emergency","required": True},
          
          {"id": "wildlife_pets", "name": "Wildlife, Livestock, Domestic pets etc","required": True},
          {"id": "collision_nearmiss", "name": "UAS collision or near miss with other air users","required": True},
          {"id": "maintenance_servicing", "name": "Maintenance and servicing","required": True},
          {"id": "crash_building", "name": "Crash into building/people","required": True},
          {"id": "security", "name": "Security","required": True},
          {"id": "insurance", "name": "Insurance","required": True},
          {"id": "data_protection", "name": "Data Protection/camera","required": True},
          {"id": "ground_hazards", "name": "Ground Hazards","required": True},
          {"id": "other_hazards", "name": "Any other Hazards/risks","required": True},
        ]
      },
      {
        "header": "Existing Control",
        "existing_control":[
          {"id": "compliance_control", "name": """
           - All drones/UAVs registered.
           - The remote pilot must not fly the aircraft in any of the circumstances described below except in accordance with a permission issued by the CAA.
           - Dont fly near airports or airfields without permission from air traffic control, Observe your drone/UAV at all times  stay 150ft (50m) away from people and property.
           - Drones/UAVs with surveillance cameras must not be flown within 50 metres of any person unless approval has been permitted, Comply with Operation Manual."""},
          
          {"id": "competence_control", "name": """
           - All drone remote pilots need to be registered with the CAA and all drones/UAVs need to have the registration number attached."""},
          
          {"id": "permission_control", "name": """
           - The pilot will seek permission in advance in line with the University procedure.
           - Off campus, permission to fly is required from the property owner.
           - Where required notification to air traffic control.
           - Approval of location and risk assessment to area must be completed."""},
          
        ]
      },
      {
        "header": "People at Risk",
        "dropdown_people":[
            {"id": "all", "name": "All in vicinity","required": True},
            {"id": "staff", "name": "Staff in vicinity","required": True},
            {"id": "students", "name": "Students in vicinity","required": True},
            {"id": "visitors", "name": "Visitors in vicinity","required": True},
            {"id": "pedestrians", "name": "Pedestrians","required": True},
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
