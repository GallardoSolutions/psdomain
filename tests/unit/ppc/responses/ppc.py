import datetime
from decimal import Decimal

null, true, false = None, True, False

json_ppc_blank_response_ok = """{
    "Configuration": {
        "PartArray": {
            "Part": [
                {
                    "partId": "62514.4",
                    "partDescription": "Gray",
                    "PartPriceArray": {
                        "PartPrice": [
                            {
                                "minQuantity": 50,
                                "discountCode": null,
                                "price": "2.37",
                                "priceUom": "EA",
                                "priceEffectiveDate": "2024-01-01T00:00:00",
                                "priceExpiryDate": "2024-12-31T00:00:00"
                            }
                        ]
                    },
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Item Color",
                    "ratio": "1",
                    "defaultPart": false,
                    "LocationIdArray": null
                },
                {
                    "partId": "62514.5",
                    "partDescription": "Blue",
                    "PartPriceArray": {
                        "PartPrice": [
                            {
                                "minQuantity": 50,
                                "discountCode": null,
                                "price": "2.37",
                                "priceUom": "EA",
                                "priceEffectiveDate": "2024-01-01T00:00:00",
                                "priceExpiryDate": "2024-12-31T00:00:00"
                            }
                        ]
                    },
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Item Color",
                    "ratio": "1",
                    "defaultPart": false,
                    "LocationIdArray": null
                },
                {
                    "partId": "62514.6",
                    "partDescription": "Red",
                    "PartPriceArray": {
                        "PartPrice": [
                            {
                                "minQuantity": 50,
                                "discountCode": null,
                                "price": "2.37",
                                "priceUom": "EA",
                                "priceEffectiveDate": "2024-01-01T00:00:00",
                                "priceExpiryDate": "2024-12-31T00:00:00"
                            }
                        ]
                    },
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Item Color",
                    "ratio": "1",
                    "defaultPart": false,
                    "LocationIdArray": null
                },
                {
                    "partId": "62514.7",
                    "partDescription": "White",
                    "PartPriceArray": {
                        "PartPrice": [
                            {
                                "minQuantity": 50,
                                "discountCode": null,
                                "price": "2.37",
                                "priceUom": "EA",
                                "priceEffectiveDate": "2024-01-01T00:00:00",
                                "priceExpiryDate": "2024-12-31T00:00:00"
                            }
                        ]
                    },
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Item Color",
                    "ratio": "1",
                    "defaultPart": false,
                    "LocationIdArray": null
                }
            ]
        },
        "LocationArray": null,
        "productId": "62514",
        "currency": "USD",
        "FobArray": {
            "Fob": [
                {
                    "fobId": "Red Wing-55066",
                    "fobPostalCode": null
                }
            ]
        },
        "fobPostalCode": null,
        "priceType": "Net"
    },
    "ErrorMessage": null
}"""

json_ppc_decorated_response_ok = """{
    "Configuration": {
        "PartArray": {
            "Part": [
                {
                    "partId": "1035ATHGLD",
                    "partDescription": "ATHLETIC GOLD",
                    "PartPriceArray": {
                        "PartPrice": [
                            {
                                "minQuantity": 144,
                                "discountCode": null,
                                "price": "2.6940",
                                "priceUom": "EA",
                                "priceEffectiveDate": "2024-02-21T00:00:00",
                                "priceExpiryDate": "2025-02-22T00:00:00"
                            }
                        ]
                    },
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Part Group",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": {
                        "LocationId": [
                            {
                                "locationId": 8
                            }
                        ]
                    }
                }
            ]
        },
        "LocationArray": {
            "Location": [
                {
                    "locationId": 8,
                    "locationName": "FRONT",
                    "DecorationArray": {
                        "Decoration": [
                            {
                                "decorationId": 1265947,
                                "decorationName": "TRANSFER",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "1.8750",
                                "decorationWidth": "4.0000",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 50,
                                "ChargeArray": {
                                    "Charge": [
                                        {
                                            "chargeId": 4389275,
                                            "chargeName": "TRANSFER",
                                            "chargeType": "Setup",
                                            "chargeDescription": "TRANSFER",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 1,
                                                        "yUom": "Colors",
                                                        "price": "40.0000",
                                                        "discountCode": null,
                                                        "repeatPrice": "20.0000",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2028-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 4389276,
                                            "chargeName": "EXTRA COLOR CHARGE",
                                            "chargeType": "Run",
                                            "chargeDescription": "EXTRA COLOR CHARGE",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 2,
                                                        "yUom": "Colors",
                                                        "price": "0.4000",
                                                        "discountCode": null,
                                                        "repeatPrice": "0.4000",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 92125150,
                                            "chargeName": "TRANSFER",
                                            "chargeType": "Run",
                                            "chargeDescription": "TRANSFER",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 144,
                                                        "xUom": "EA",
                                                        "yMinQty": 1,
                                                        "yUom": "Colors",
                                                        "price": "1.2000",
                                                        "discountCode": null,
                                                        "repeatPrice": "1.2000",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2023-03-31T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        }
                                    ]
                                },
                                "decorationUnitsIncluded": 1,
                                "decorationUnitsIncludedUom": "Colors",
                                "decorationUnitsMax": 4,
                                "defaultDecoration": false,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            },
                            {
                                "decorationId": 1265948,
                                "decorationName": "EMBROIDERY",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.2500",
                                "decorationWidth": "4.5000",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": {
                                    "Charge": [
                                        {
                                            "chargeId": 4389282,
                                            "chargeName": "ADDITIONAL TAPE CHARGE",
                                            "chargeType": "Setup",
                                            "chargeDescription": "ADDITIONAL TAPE CHARGE",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 7000,
                                                        "yUom": "Stitches",
                                                        "price": "28.0000",
                                                        "discountCode": null,
                                                        "repeatPrice": "28.0000",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 4389283,
                                            "chargeName": "EXTRA STITCHES CHARGE",
                                            "chargeType": "Run",
                                            "chargeDescription": "EXTRA STITCHES CHARGE",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 1000,
                                                        "yUom": "Stitches",
                                                        "price": "0.2800",
                                                        "discountCode": null,
                                                        "repeatPrice": "0.2800",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 4389284,
                                            "chargeName": "METALLIC THREAD",
                                            "chargeType": "Run",
                                            "chargeDescription": "METALLIC THREAD",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 1,
                                                        "yUom": "Other",
                                                        "price": "0.2800",
                                                        "discountCode": null,
                                                        "repeatPrice": "0.2800",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 92125151,
                                            "chargeName": "EMBROIDERY",
                                            "chargeType": "Run",
                                            "chargeDescription": "EMBROIDERY",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 144,
                                                        "xUom": "EA",
                                                        "yMinQty": 1,
                                                        "yUom": "Stitches",
                                                        "price": "1.8000",
                                                        "discountCode": null,
                                                        "repeatPrice": "1.8000",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2023-03-31T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        }
                                    ]
                                },
                                "decorationUnitsIncluded": 7000,
                                "decorationUnitsIncludedUom": "Stitches",
                                "decorationUnitsMax": 40000,
                                "defaultDecoration": true,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            },
                            {
                                "decorationId": 1399509,
                                "decorationName": "3D EMBROIDERY",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.2500",
                                "decorationWidth": "4.5000",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": {
                                    "Charge": [
                                        {
                                            "chargeId": 4389286,
                                            "chargeName": "3D EMBROIDERY",
                                            "chargeType": "Run",
                                            "chargeDescription": "3D EMBROIDERY",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 144,
                                                        "xUom": "EA",
                                                        "yMinQty": 1,
                                                        "yUom": "Stitches",
                                                        "price": "2.9100",
                                                        "discountCode": null,
                                                        "repeatPrice": "2.9100",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        },
                                        {
                                            "chargeId": 4389288,
                                            "chargeName": "EXTRA STITCHES CHARGE",
                                            "chargeType": "Run",
                                            "chargeDescription": "EXTRA STITCHES CHARGE",
                                            "ChargePriceArray": {
                                                "ChargePrice": [
                                                    {
                                                        "xMinQty": 1,
                                                        "xUom": "EA",
                                                        "yMinQty": 1000,
                                                        "yUom": "Stitches",
                                                        "price": "0.4320",
                                                        "discountCode": null,
                                                        "repeatPrice": "0.4320",
                                                        "repeatDiscountCode": null,
                                                        "priceEffectiveDate": "2020-02-26T00:00:00",
                                                        "priceExpiryDate": "2030-01-01T00:00:00"
                                                    }
                                                ]
                                            },
                                            "chargesAppliesLTM": null,
                                            "chargesPerLocation": null,
                                            "chargesPerColor": null
                                        }
                                    ]
                                },
                                "decorationUnitsIncluded": 7000,
                                "decorationUnitsIncludedUom": "Stitches",
                                "decorationUnitsMax": 40000,
                                "defaultDecoration": false,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            }
                        ]
                    },
                    "decorationsIncluded": 1,
                    "defaultLocation": true,
                    "maxDecoration": 1,
                    "minDecoration": 0,
                    "locationRank": 1
                }
            ]
        },
        "productId": "1035",
        "currency": "USD",
        "FobArray": {
            "Fob": [
                {
                    "fobId": "1",
                    "fobPostalCode": "33777"
                },
                {
                    "fobId": "12",
                    "fobPostalCode": "L6S6H2"
                }
            ]
        },
        "fobPostalCode": null,
        "priceType": "Net"
    },
    "ErrorMessage": null
}"""

json_ppc_kit_decorated_response_ok = """{
    "Configuration": {
        "PartArray": {
            "Part": [
                {
                    "partId": "0BOW-BLK",
                    "partDescription": null,
                    "PartPriceArray": null,
                    "partGroup": 3,
                    "nextPartGroup": 4,
                    "partGroupRequired": true,
                    "partGroupDescription": "RIBBON",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": null
                },
                {
                    "partId": "0CCC-BLK",
                    "partDescription": null,
                    "PartPriceArray": null,
                    "partGroup": 4,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "CANDY",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": null
                },
                {
                    "partId": "0CCC-ORN",
                    "partDescription": null,
                    "PartPriceArray": null,
                    "partGroup": 4,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "CANDY",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": null
                },
                {
                    "partId": "0BOW-WHT",
                    "partDescription": null,
                    "PartPriceArray": null,
                    "partGroup": 3,
                    "nextPartGroup": 4,
                    "partGroupRequired": true,
                    "partGroupDescription": "RIBBON",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": null
                },
                {
                    "partId": "0MS22-CLR",
                    "partDescription": "CLEAR",
                    "PartPriceArray": null,
                    "partGroup": 2,
                    "nextPartGroup": 3,
                    "partGroupRequired": true,
                    "partGroupDescription": "Part Group",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": null
                },
                {
                    "partId": "7133ORN",
                    "partDescription": "ORANGE",
                    "PartPriceArray": null,
                    "partGroup": 1,
                    "nextPartGroup": null,
                    "partGroupRequired": true,
                    "partGroupDescription": "Part Group",
                    "ratio": "1.00",
                    "defaultPart": null,
                    "LocationIdArray": {
                        "LocationId": [
                            {
                                "locationId": 53
                            },
                            {
                                "locationId": 54
                            }
                        ]
                    }
                }
            ]
        },
        "LocationArray": {
            "Location": [
                {
                    "locationId": 53,
                    "locationName": "SIDE1",
                    "DecorationArray": {
                        "Decoration": [
                            {
                                "decorationId": 35683890,
                                "decorationName": "SILK SCREEN",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.0000",
                                "decorationWidth": "3.0000",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": null,
                                "decorationUnitsIncluded": 1,
                                "decorationUnitsIncludedUom": "Colors",
                                "decorationUnitsMax": 4,
                                "defaultDecoration": true,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            },
                            {
                                "decorationId": 35683891,
                                "decorationName": "LASER ENGRAVE",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.0000",
                                "decorationWidth": "1.7500",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": null,
                                "decorationUnitsIncluded": 1,
                                "decorationUnitsIncludedUom": "Other",
                                "decorationUnitsMax": 1,
                                "defaultDecoration": false,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            }
                        ]
                    },
                    "decorationsIncluded": 1,
                    "defaultLocation": true,
                    "maxDecoration": 1,
                    "minDecoration": 0,
                    "locationRank": 1
                },
                {
                    "locationId": 54,
                    "locationName": "SIDE2",
                    "DecorationArray": {
                        "Decoration": [
                            {
                                "decorationId": 35684698,
                                "decorationName": "SILK SCREEN",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.0000",
                                "decorationWidth": "3.0000",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": null,
                                "decorationUnitsIncluded": 1,
                                "decorationUnitsIncludedUom": "Colors",
                                "decorationUnitsMax": 4,
                                "defaultDecoration": true,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            },
                            {
                                "decorationId": 35684699,
                                "decorationName": "LASER ENGRAVE",
                                "decorationGeometry": "Rectangle",
                                "decorationHeight": "2.0000",
                                "decorationWidth": "1.7500",
                                "decorationDiameter": null,
                                "decorationUom": "Inches",
                                "allowSubForDefaultLocation": false,
                                "allowSubForDefaultMethod": false,
                                "itemPartQuantityLTM": 0,
                                "ChargeArray": null,
                                "decorationUnitsIncluded": 1,
                                "decorationUnitsIncludedUom": "Other",
                                "decorationUnitsMax": 1,
                                "defaultDecoration": false,
                                "leadTime": 3,
                                "rushLeadTime": 1
                            }
                        ]
                    },
                    "decorationsIncluded": 1,
                    "defaultLocation": false,
                    "maxDecoration": 1,
                    "minDecoration": 0,
                    "locationRank": 1
                }
            ]
        },
        "productId": "95246",
        "currency": "USD",
        "FobArray": {
            "Fob": [
                {
                    "fobId": "17",
                    "fobPostalCode": "08031"
                },
                {
                    "fobId": "12",
                    "fobPostalCode": "L6S6H2"
                }
            ]
        },
        "fobPostalCode": null,
        "priceType": "Net"
    },
    "ErrorMessage": null
} """

json_ppc_empty_response = """{
    "Configuration": {
        "PartArray": null,
        "LocationArray": null,
        "productId": null,
        "currency": "USD",
        "FobArray": null,
        "fobPostalCode": null,
        "priceType": "Customer"
    },
    "ErrorMessage": null
}"""

ppc_inch_instead_of_inches_response = {
    'Configuration': {
        'PartArray': {
            'Part': [
                {
                    'partId': '0HM1031TNGN10',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN11',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN12',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN13',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN14',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN8',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                },
                {
                    'partId': '0HM1031TNGN9',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('72.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('71.6100'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('71.4900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('71.0000'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('70.8500'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2023, 1, 1, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 245
                            }
                        ]
                    }
                }
            ]
        },
        'LocationArray': {
            'Location': [
                {
                    'locationId': 245,
                    'locationName': 'STRAP',
                    'DecorationArray': {
                        'Decoration': [
                            {
                                'decorationId': 33105834,
                                'decorationName': 'SUBLIMATED PATCH',
                                'decorationGeometry': 'Other',
                                'decorationHeight': None,
                                'decorationWidth': None,
                                'decorationDiameter': None,
                                'decorationUom': 'Inch',
                                'allowSubForDefaultLocation': False,
                                'allowSubForDefaultMethod': False,
                                'itemPartQuantityLTM': 0,
                                'ChargeArray': {
                                    'Charge': [
                                        {
                                            'chargeId': 99636467,
                                            'chargeName': 'SUBLIMATED PATCH',
                                            'chargeDescription': 'SUBLIMATED PATCH',
                                            'chargeType': 'Run',
                                            'ChargePriceArray': {
                                                'ChargePrice': [
                                                    {
                                                        'xMinQty': 50,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('4.8800'),
                                                        'discountCode': 'C',
                                                        'repeatPrice': Decimal('4.8800'),
                                                        'repeatDiscountCode': 'C',
                                                        'priceEffectiveDate': datetime.datetime(2023, 7, 18, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2030, 7, 23, 0, 0)
                                                    },
                                                    {
                                                        'xMinQty': 100,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('4.8000'),
                                                        'discountCode': 'C',
                                                        'repeatPrice': Decimal('4.8000'),
                                                        'repeatDiscountCode': 'C',
                                                        'priceEffectiveDate': datetime.datetime(2023, 7, 18, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2030, 7, 23, 0, 0)
                                                    },
                                                    {
                                                        'xMinQty': 250,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('4.7700'),
                                                        'discountCode': 'C',
                                                        'repeatPrice': Decimal('4.7700'),
                                                        'repeatDiscountCode': 'C',
                                                        'priceEffectiveDate': datetime.datetime(2023, 7, 18, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2030, 7, 23, 0, 0)
                                                    },
                                                    {
                                                        'xMinQty': 500,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('4.6600'),
                                                        'discountCode': 'C',
                                                        'repeatPrice': Decimal('4.6600'),
                                                        'repeatDiscountCode': 'C',
                                                        'priceEffectiveDate': datetime.datetime(2023, 7, 18, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2030, 7, 23, 0, 0)
                                                    },
                                                    {
                                                        'xMinQty': 1000,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('4.6400'),
                                                        'discountCode': 'C',
                                                        'repeatPrice': Decimal('4.6400'),
                                                        'repeatDiscountCode': 'C',
                                                        'priceEffectiveDate': datetime.datetime(2023, 7, 18, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2030, 7, 23, 0, 0)
                                                    }
                                                ]
                                            },
                                            'chargesAppliesLTM': None,
                                            'chargesPerLocation': None,
                                            'chargesPerColor': None
                                        }
                                    ]
                                },
                                'decorationUnitsIncluded': 1,
                                'decorationUnitsIncludedUom': 'Other',
                                'decorationUnitsMax': 4,
                                'defaultDecoration': True,
                                'leadTime': 3,
                                'rushLeadTime': 1
                            }
                        ]
                    },
                    'decorationsIncluded': 1,
                    'defaultLocation': True,
                    'maxDecoration': 1,
                    'minDecoration': 0,
                    'locationRank': 1
                }
            ]
        },
        'productId': 'HM1031',
        'currency': 'USD',
        'FobArray': {
            'Fob': [
                {
                    'fobId': '1',
                    'fobPostalCode': '33777'
                },
                {
                    'fobId': '12',
                    'fobPostalCode': 'L6S6H2'
                }
            ]
        },
        'priceType': 'List'
    },
    'ErrorMessage': None
}

ppc_decoration_arr_non_existing = {
    'Configuration': {
        'PartArray': {
            'Part': [
                {
                    'partId': '0PATCH19WHT',
                    'partDescription': None,
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 50,
                                'price': Decimal('36.8600'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2022, 3, 28, 0, 0),
                                'priceExpiryDate': datetime.datetime(2028, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 100,
                                'price': Decimal('29.6600'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2022, 3, 28, 0, 0),
                                'priceExpiryDate': datetime.datetime(2028, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 250,
                                'price': Decimal('26.8600'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2022, 3, 28, 0, 0),
                                'priceExpiryDate': datetime.datetime(2028, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('23.9900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2022, 3, 28, 0, 0),
                                'priceExpiryDate': datetime.datetime(2028, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 1000,
                                'price': Decimal('23.9900'),
                                'discountCode': 'C',
                                'priceUom': 'EA',
                                'priceEffectiveDate': datetime.datetime(2022, 3, 28, 0, 0),
                                'priceExpiryDate': datetime.datetime(2028, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': 2,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 242
                            }
                        ]
                    }
                },
                {
                    'partId': '3255BLK',
                    'partDescription': 'BLACK',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                },
                {
                    'partId': '3255GRF',
                    'partDescription': 'FOREST GREEN',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                },
                {
                    'partId': '3255NAT',
                    'partDescription': 'NATURAL',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                },
                {
                    'partId': '3255NAV',
                    'partDescription': 'NAVY BLUE',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                },
                {
                    'partId': '3255RED',
                    'partDescription': 'RED',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                },
                {
                    'partId': '3255ROY',
                    'partDescription': 'ROYAL BLUE',
                    'PartPriceArray': None,
                    'partGroup': 2,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'TOTE BAG',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': None
                }
            ]
        },
        'LocationArray': {
            'Location': [
                {
                    'locationId': 242,
                    'locationName': 'POCKET',
                    'DecorationArray': None,
                    'decorationsIncluded': 1,
                    'defaultLocation': True,
                    'maxDecoration': 1,
                    'minDecoration': 0,
                    'locationRank': 1
                }
            ]
        },
        'productId': '3255PAT',
        'currency': 'USD',
        'FobArray': {
            'Fob': [
                {
                    'fobId': '1',
                    'fobPostalCode': '33777'
                },
                {
                    'fobId': '12',
                    'fobPostalCode': 'L6S6H2'
                }
            ]
        },
        'priceType': 'List'
    },
    'ErrorMessage': None
}

ppc_unknown_price_uom_response = {
    'Configuration': {
        'PartArray': {
            'Part': [
                {
                    'partId': '17286BLK',
                    'partDescription': 'BLACK',
                    'PartPriceArray': {
                        'PartPrice': [
                            {
                                'minQuantity': 200,
                                'price': Decimal('2.4200'),
                                'discountCode': 'C',
                                'priceUom': 'C',
                                'priceEffectiveDate': datetime.datetime(2024, 5, 22, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            },
                            {
                                'minQuantity': 500,
                                'price': Decimal('2.1000'),
                                'discountCode': 'C',
                                'priceUom': 'C',
                                'priceEffectiveDate': datetime.datetime(2024, 5, 22, 0, 0),
                                'priceExpiryDate': datetime.datetime(2030, 1, 1, 0, 0)
                            }
                        ]
                    },
                    'partGroup': 1,
                    'nextPartGroup': None,
                    'partGroupRequired': True,
                    'partGroupDescription': 'Part Group',
                    'ratio': Decimal('1.00'),
                    'defaultPart': None,
                    'LocationIdArray': {
                        'LocationId': [
                            {
                                'locationId': 56
                            }
                        ]
                    }
                }
            ]
        },
        'LocationArray': {
            'Location': [
                {
                    'locationId': 56,
                    'locationName': 'BARREL',
                    'DecorationArray': {
                        'Decoration': [
                            {
                                'decorationId': 3189501,
                                'decorationName': 'LASER ENGRAVE',
                                'decorationGeometry': 'Rectangle',
                                'decorationHeight': Decimal('0.7500'),
                                'decorationWidth': Decimal('2.1250'),
                                'decorationDiameter': None,
                                'decorationUom': 'Inches',
                                'allowSubForDefaultLocation': False,
                                'allowSubForDefaultMethod': False,
                                'itemPartQuantityLTM': 0,
                                'ChargeArray': {
                                    'Charge': [
                                        {
                                            'chargeId': 7382268,
                                            'chargeName': 'LASER ENGRAVE',
                                            'chargeDescription': 'LASER ENGRAVE',
                                            'chargeType': 'Setup',
                                            'ChargePriceArray': {
                                                'ChargePrice': [
                                                    {
                                                        'xMinQty': 1,
                                                        'xUom': 'EA',
                                                        'yMinQty': 1,
                                                        'yUom': 'Other',
                                                        'price': Decimal('45.0000'),
                                                        'discountCode': 'G',
                                                        'repeatPrice': Decimal('45.0000'),
                                                        'repeatDiscountCode': 'G',
                                                        'priceEffectiveDate': datetime.datetime(2021, 9, 13, 0, 0),
                                                        'priceExpiryDate': datetime.datetime(2026, 1, 1, 0, 0)
                                                    }
                                                ]
                                            },
                                            'chargesAppliesLTM': None,
                                            'chargesPerLocation': None,
                                            'chargesPerColor': None
                                        }
                                    ]
                                },
                                'decorationUnitsIncluded': 1,
                                'decorationUnitsIncludedUom': 'Other',
                                'decorationUnitsMax': 1,
                                'defaultDecoration': True,
                                'leadTime': 3,
                                'rushLeadTime': 1
                            }
                        ]
                    },
                    'decorationsIncluded': 1,
                    'defaultLocation': True,
                    'maxDecoration': 1,
                    'minDecoration': 0,
                    'locationRank': 1
                }
            ]
        },
        'productId': '17286',
        'currency': 'USD',
        'FobArray': {
            'Fob': [
                {
                    'fobId': '69',
                    'fobPostalCode': '12010'
                },
                {
                    'fobId': '12',
                    'fobPostalCode': 'L6S6H2'
                }
            ]
        },
        'priceType': 'List'
    },
    'ErrorMessage': None
}

ppc_square_inches_response = b'{"ErrorMessage":null,"Configuration":{"PartArray":{"Part":[{"partId":"EL225-47-00","partDescription":"EL225-10W FSC WOOD SPKR, Wood","PartPriceArray":{"PartPrice":[{"minQuantity":4,"discountCode":"C","price":"74.09","priceUom":"EA","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"},{"minQuantity":12,"discountCode":"C","price":"71.82","priceUom":"EA","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"},{"minQuantity":36,"discountCode":"C","price":"69.54","priceUom":"EA","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"},{"minQuantity":72,"discountCode":"C","price":"64.99","priceUom":"EA","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"}]},"partGroup":1,"nextPartGroup":null,"partGroupRequired":true,"partGroupDescription":"Main Part, EL225-10W FSC WOOD SPKR","ratio":"1.0","defaultPart":true,"LocationIdArray":{"LocationId":[{"locationId":130}]}}]},"LocationArray":{"Location":[{"locationId":130,"locationName":"Top","DecorationArray":{"Decoration":[{"decorationId":3,"decorationName":"Laser","decorationGeometry":"Rectangle","decorationHeight":"2.0000","decorationWidth":"4.0000","decorationDiameter":"0","decorationUom":"Inches","allowSubForDefaultLocation":true,"allowSubForDefaultMethod":true,"itemPartQuantityLTM":2,"ChargeArray":{"Charge":[{"chargeId":24,"chargeName":"Setup Charge: Laser","chargeType":"Setup","chargeDescription":"Setup Charge: Laser","ChargePriceArray":{"ChargePrice":[{"xMinQty":1,"xUom":"EA","yMinQty":1,"yUom":"Locations","price":"60.00","discountCode":"G","repeatPrice":"0","repeatDiscountCode":"G","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"}]},"chargesAppliesLTM":false,"chargesPerLocation":0,"chargesPerColor":0},{"chargeId":26,"chargeName":"Laser Additional Location Charge","chargeType":"Run","chargeDescription":"Laser Additional Location Charge","ChargePriceArray":{"ChargePrice":[{"xMinQty":1,"xUom":"EA","yMinQty":1,"yUom":"Other","price":"1.20","discountCode":"G","repeatPrice":"1.20","repeatDiscountCode":"G","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"}]},"chargesAppliesLTM":false,"chargesPerLocation":0,"chargesPerColor":0}]},"decorationUnitsIncluded":1,"decorationUnitsIncludedUom":"Colors","decorationUnitsMax":2,"defaultDecoration":true,"leadTime":3,"rushLeadTime":1},{"decorationId":20,"decorationName":"TruColor","decorationGeometry":"Rectangle","decorationHeight":"2.0000","decorationWidth":"6.0000","decorationDiameter":"0","decorationUom":"Inches","allowSubForDefaultLocation":true,"allowSubForDefaultMethod":true,"itemPartQuantityLTM":2,"ChargeArray":{"Charge":[{"chargeId":134,"chargeName":"Set-up TruColor","chargeType":"Setup","chargeDescription":"Set-up TruColor","ChargePriceArray":{"ChargePrice":[{"xMinQty":1,"xUom":"EA","yMinQty":1,"yUom":"Locations","price":"60.00","discountCode":"G","repeatPrice":"0","repeatDiscountCode":"G","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"}]},"chargesAppliesLTM":false,"chargesPerLocation":0,"chargesPerColor":0},{"chargeId":137,"chargeName":"TruColor Large Imprint","chargeType":"Run","chargeDescription":"TruColor Large Imprint","ChargePriceArray":{"ChargePrice":[{"xMinQty":1,"xUom":"EA","yMinQty":1,"yUom":"Inches","price":"0.24","discountCode":"G","repeatPrice":"0.24","repeatDiscountCode":"G","priceEffectiveDate":"2024-01-01T00:00:00","priceExpiryDate":"2024-12-31T00:00:00"}]},"chargesAppliesLTM":false,"chargesPerLocation":0,"chargesPerColor":0}]},"decorationUnitsIncluded":3,"decorationUnitsIncludedUom":"SquareInches","decorationUnitsMax":12,"defaultDecoration":false,"leadTime":3,"rushLeadTime":1}]},"decorationsIncluded":1,"defaultLocation":true,"maxDecoration":1,"minDecoration":1,"locationRank":1}]},"productId":"EL225","currency":"USD","FobArray":{"Fob":[{"fobId":"1","fobPostalCode":"14072"}]},"fobPostalCode":null,"priceType":"List"}}'  # noqa

cutter_example = {
    'partId': '193804968925',
    'partDescription': 'M',
    'PartPriceArray': {
        'PartPrice': [
            {
                'minQuantity': 1,
                'price': 75.00,
                'discountCode': None,
                'priceUom': 'EA',
                'priceEffectiveDate': datetime.datetime(2024, 11, 24, 22, 54, 3, 659293),
                'priceExpiryDate': datetime.datetime(2025, 6, 30, 7, 0)
            }
        ]
    },
    'partGroup': 1,
    'partGroupRequired': None,
    'partGroupDescription': None,
    'ratio': None,
    'defaultPart': None,
    'LocationIdArray': None,
}

bambams_example = {
    "ErrorMessage": null,
    "Configuration":
        {
            "PartArray": {
                "Part": [
                    {"partId": "CHU-4149BKR-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}},
                    {"partId": "CHU-4149BKW-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}},
                    {"partId": "CHU-4149CHB-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}},
                    {"partId": "CHU-4149CYW-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}},
                    {"partId": "CHU-4149NVW-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}},
                    {"partId": "CHU-4149WHN-SP",
                     "partDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "PartPriceArray": {"PartPrice": [
                         {"minQuantity": 24, "discountCode": "R", "price": "19.69", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 48, "discountCode": "R", "price": "17.14", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 144, "discountCode": "R", "price": "14.80", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"},
                         {"minQuantity": 600, "discountCode": "R", "price": "13.00", "priceUom": "EA",
                          "priceEffectiveDate": null,
                          "priceExpiryDate": "2027-04-12T07:00:00Z"}]}, "partGroup": 1, "nextPartGroup": null,
                     "partGroupRequired": false,
                     "partGroupDescription": "Sports Ripstop with Sandwich Trim Cap (Domestically Decorated)",
                     "ratio": "0",
                     "defaultPart": null, "LocationIdArray": {"LocationId": [{"locationId": 1}]}}]},
            "LocationArray": {
                "Location": [
                    {
                        "locationId": 1, "locationName":
                        "Front",
                        "DecorationArray": {
                            "Decoration": [
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null},
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null},
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null},
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null},
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null},
                                {"decorationId": 14, "decorationName": "Embroidery", "decorationGeometry": "Other",
                                 "decorationHeight": "3.94",
                                 "decorationWidth": "2.17", "decorationDiameter": null, "decorationUom": "Inches",
                                 "allowSubForDefaultLocation": false, "allowSubForDefaultMethod": false,
                                 "itemPartQuantityLTM": null,
                                 "ChargeArray": null, "decorationUnitsIncluded": null,
                                 "decorationUnitsIncludedUom": null,
                                 "decorationUnitsMax": null, "defaultDecoration": false, "leadTime": null,
                                 "rushLeadTime": null}]},
                        "decorationsIncluded": 0, "defaultLocation": false, "maxDecoration": None,
                        "minDecoration": None,
                        "locationRank": 1}
                ]
            },
            "productId": "CHU-4149-SP", "currency": "USD",
            "FobArray": {
                "Fob": [{"fobId": "3", "fobPostalCode": "77474"}]
            },
            "fobPostalCode": null,
            "priceType": "List"
        }
}
