PreFlightTemplate = [
{
  "title": "Pre-flight Actions",
  "header": "Procedures to follow on the lead up to take-off.",
  "form": {
    "sections": [
      {
        "header": "Before Power-Up",
        "fields": [
            {"id": "uasAssembly", "name": "No issues arising from UAS assembly", "value": False, "type": "checkbox", "required": False},
            {"id": "batteriesCharged", "name": "All batteries charged", "value": False, "type": "checkbox", "required": False},
            {"id": "areaOfOperationCheck", "name": "Area of operations within expected parameters", "value": False, "type": "checkbox", "required": False},
            {"id": "noAdverseWeather", "name": "No adverse weather conditions", "value": False, "type": "checkbox", "required": False},
            {"id": "rthHeightSet", "name": "RTH height set to appropriate value for site", "value": False, "type": "checkbox", "required": False},
            {"id": "geofenceSet", "name": "Geofence setting disabled or set to appropriate value for site", "value": False, "type": "checkbox", "required": False}
        ]
      },
      {
        "header": "After Power-Up",
        "fields": [
            {"id": "mobileConnected", "name": "Mobile device connected to controller", "value": False, "type": "checkbox", "required": False},
            {"id": "dataLinkEstablished", "name": "Data link established between controller and RPA", "value": False, "type": "checkbox", "required": False},
            {"id": "telemetryDisplayed", "name": "Telemetry is displayed successfully via controller/mobile interface", "value": False, "type": "checkbox", "required": False},
            {"id": "gpsCoverage", "name": "GPS coverage is sufficient", "value": False, "type": "checkbox", "required": False},
            {"id": "flightModeSelected", "name": "Correct flight mode is selected at the controller", "value": False, "type": "checkbox", "required": False},
            {"id": "selfDiagnosticComplete", "name": "RPA self-diagnostic sequence completes successfully", "value": False, "type": "checkbox", "required": False}
        ]
      },
      {
        "header": "At Take off",
        "fields": [
            {"id": "crewInPosition", "name": "All crew are in position", "value": False, "type": "checkbox", "required": False},
            {"id": "areaClear", "name": "Ground area and airspace are clear", "value": False, "type": "checkbox", "required": False},
            {"id": "pilotCallsClear", "name": "Pilot calls Clear", "value": False, "type": "checkbox", "required": False},
            {"id": "crewRepliesClear", "name": "Designated crew member confirms by replying Clear", "value": False, "type": "checkbox", "required": False},
            {"id": "pilotCallsTakeoff", "name": "Pilot calls Aircraft taking off", "value": False, "type": "checkbox", "required": False},
            {"id": "rpaTo5m", "name": "Pilot takes RPA to 5m ASL", "value": False, "type": "checkbox", "required": False},
            {"id": "checkControlsPayload", "name": "Pilot checks pitch, roll, yaw and payload operation", "value": False, "type": "checkbox", "required": False},
            {"id": "ledsWorking", "name": "LEDs working correctly", "value": False, "type": "checkbox", "required": False}
        ]
      }
    ]
  }
}
]