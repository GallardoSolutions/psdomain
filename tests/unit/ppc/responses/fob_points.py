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

snugs_fob_point_united_states_response = {
    "ErrorMessage": None,
    "FobPointArray": {
        "FobPoint": [
            {
                "fobId": "23",
                "fobPostalCode": "79906",
                "fobCity": "El Paso",
                "fobState": "TX",
                "fobCountry": "UNITED STATES",
                "CurrencySupportedArray": {
                    "CurrencySupported": [
                        {
                            "currency": "USD"
                        }
                    ]
                },
                "ProductArray": {
                    "Product": [
                        {
                            "productId": "LP12P-PB1"
                        }
                    ]
                }
            }
        ]
    }
}


pcna_fob_point_usa_response = {
    "ErrorMessage": None,
    "FobPointArray": {
        "FobPoint": [
            {
                "fobId": "15068",
                "fobPostalCode": "15068",
                "fobCity": "New Kensington",
                "fobState": "PA",
                "fobCountry": "USA",
                "CurrencySupportedArray": {
                    "CurrencySupported": [
                        {
                            "currency": "CAD"
                        },
                        {
                            "currency": "USD"
                        }
                    ]
                },
                "ProductArray": {
                    "Product": [
                        {
                            "productId": "0011-86"
                        }
                    ]
                }
            }
        ]
    }
}
