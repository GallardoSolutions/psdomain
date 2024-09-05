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
                                "itemPartQuantityLTM": 0,
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
