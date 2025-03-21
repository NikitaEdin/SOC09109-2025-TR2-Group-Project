LoadingListSafetyKitTemplate = [
{
  "title": "Loading List - Safety Kit",
  "header": "Ensure all safety kit items are checked before proceeding.",
  "form": {
    "sections": [
      {
        "header": "Medical Equipment",
        "fields": [
          # Can add more in the future
          {"id": "firstaid", "name": "First aid kit", "value": "", "type": "checkbox", "required": False}
        ]
      },
      {
        "header": "Fire & Safety Equipment",
        "fields": [
          {"id": "fireextinguisher", "name": "Fire extinguisher", "value": "", "type": "checkbox", "required": False},
          {"id": "ppe", "name": "PPE Clothing", "value": "", "type": "checkbox", "required": False},
          {"id": "anemometer", "name": "Anemometer (Wind Speed)", "value": "", "type": "checkbox", "required": False},
          {"id": "landingpad", "name": "Landing pad", "value": "", "type": "checkbox", "required": False},
          {"id": "cone", "name": "Cones", "value": "", "type": "checkbox", "required": False},
          {"id": "radio", "name": "Radios", "value": "", "type": "checkbox", "required": False},
          {"id": "phone", "name": "Mobile Phone", "value": "", "type": "checkbox", "required": False}
        ]
      }
    ]
  }
}
]
