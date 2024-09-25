json_response_ok = """{
    "FobPointArray": {
        "FobPoint": [
            {
                "fobId": "1",
                "fobPostalCode": "33777",
                "fobCity": "Largo",
                "fobState": "FL",
                "fobCountry": "US",
                "CurrencySupportedArray": {
                    "CurrencySupported": [
                        {
                            "currency": "USD"
                        },
                        {
                            "currency": "CAD"
                        }
                    ]
                },
                "ProductArray": {
                    "Product": [
                        {
                            "productId": "1035"
                        },
                        {
                            "productId": "2799"
                        },
                        {
                            "productId": "20102"
                        }
                    ]
                }
            }
        ]
    },
    "ErrorMessage": null
}"""

snugz_fob_point_china_response = {
    'FobPointArray': {
        'FobPoint': [
            {
                'fobId': '5',
                'fobCity': None,
                'fobState': 'China',
                'fobPostalCode': 'Direct',
                'fobCountry': 'CHINA',
                'CurrencySupportedArray': {
                    'CurrencySupported': [
                        {
                            'currency': 'USD'
                        }
                    ]
                },
                'ProductArray': {
                    'Product': [
                        {
                            'productId': 'ILRP34MST'
                        }
                    ]
                }
            }
        ]
    },
    'ErrorMessage': None
}
