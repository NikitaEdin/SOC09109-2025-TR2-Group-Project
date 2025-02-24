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
          {"id": "flightdate", "name": "Flight Date", "value": "", "type": "date", "required": True}
        ]
      },
      {
        "header": "Preparation Information",
        "fields": [
          {"id": "preparedby", "name": "Prepared By", "value": "", "type": "text"},
          {"id": "prepareddate", "name": "Prepared Date", "value": "", "type": "date"}
        ]
      },
      {
        "header": "Observations",
        "fields": [
          {"id": "airspaceclass", "name": "Airspace Class", "value": "", "type": "text"},
          {"id": "airspaceobservations", "name": "Airspace Observations", "value": "", "type": "textarea"},
          {"id": "airspacesources", "name": "Airspace Sources", "value": "", "type": "textarea"},
          {"id": "groundobservations", "name": "Ground Observations", "value": "", "type": "textarea"},
          {"id": "groundsources", "name": "Ground Sources", "value": "", "type": "textarea"},
          {"id": "watherobservations", "name": "Weather Observations", "value": "", "type": "textarea"},
          {"id": "weathersources", "name": "Weather Sources", "value": "", "type": "textarea"}
        ]
      }
    ]
  }
}
]
