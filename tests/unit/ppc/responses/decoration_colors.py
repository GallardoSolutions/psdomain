json_decoration_colors_response_ok = """{
    "DecorationColors": {
        "productId": "BT18",
        "locationId": 1,
        "pmsMatch": true,
        "fullColor": true,
        "ColorArray": {
            "Color": [
                {
                    "colorName": "Standard",
                    "hex": null,
                    "approximatePms": null,
                    "standardColorName": null
                }
            ]
        },
        "DecorationMethodArray": {
            "DecorationMethod": [
                {
                    "decorationId": 1,
                    "decorationName": "Embroidery"
                },
                {
                    "decorationId": 2,
                    "decorationName": "Imprinted"
                }
            ]
        }
    },
    "ErrorMessage": null
}"""


decoration_colors_response_pms_match_and_full_color_null = {
    'DecorationColors': {
        'ColorArray': {
            'Color': [
                {
                    'colorId': '563',
                    'colorName': 'CMYK'
                }
            ]
        },
        'productId': 'AM01',
        'locationId': 16986,
        'DecorationMethodArray': {
            'DecorationMethod': [
                {
                    'decorationId': 115,
                    'decorationName': '4 Color'
                }
            ]
        },
        'pmsMatch': None,
        'fullColor': None
    },
    'ErrorMessage': None
}
