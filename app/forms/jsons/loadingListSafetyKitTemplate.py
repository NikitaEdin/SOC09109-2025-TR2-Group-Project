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
          {"id": "firstaid", "name": "First aid kit", "value": False, "type": "checkbox", "required": True}
        ]
      },
      {
        "header": "Fire & Safety Equipment",
        "fields": [
          {"id": "fireextinguisher", "name": "Fire extinguisher", "value": False, "type": "checkbox", "required": True},
          {"id": "ppe", "name": "PPE Clothing", "value": False, "type": "checkbox", "required": True},
          {"id": "anemometer", "name": "Anemometer (Wind Speed)", "value": False, "type": "checkbox", "required": True},
          {"id": "landingpad", "name": "Landing pad", "value": False, "type": "checkbox", "required": True},
          {"id": "cone", "name": "Cones", "value": False, "type": "checkbox", "required": True},
          {"id": "radio", "name": "Radios", "value": False, "type": "checkbox", "required": True},
          {"id": "phone", "name": "Mobile Phone", "value": False, "type": "checkbox", "required": True}
        ]
      }
    ]
  }
}
]
