json_locations_response_ok = """{
    "AvailableLocationArray": {
        "AvailableLocation": [
            {
                "locationId": 8,
                "locationName": "FRONT"
            }
        ]
    },
    "ErrorMessage": null
}"""

start_location_name_empty_response = {
    'AvailableLocationArray': {
        'AvailableLocation': [
            {
                'locationId': 0,
                'locationName': None
            }
        ]
    },
    'ErrorMessage': {
        'code': 204,
        'description': '204: No Content Found'
    }
}
