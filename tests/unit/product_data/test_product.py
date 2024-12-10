from datetime import datetime
from decimal import Decimal

from psdomain.model.product_data.common import FobPoint
from psdomain.model.product_data.v_2_0_0 import ProductResponseV200


def test_fob_city_can_be_none():
    data = {
        'fobId': '5',
        'fobCity': None,
        'fobState': 'China',
        'fobPostalCode': 'Direct',
        'fobCountry': 'US'
    }
    fob_point = FobPoint.model_validate(data)
    assert fob_point.fobCity is None


def test_product_v200():
    now = datetime.now()
    data = {
        'Product': {
            'productId': 'SK800D',
            'productName': 'IMPORT Custom Digital Sublimation Crew Socks',
            'description': [
                'Need a fun branded sock for your next event? Our crew-style jacquard sock is perfect for full '
                'customization. You can even add a custom printed tag or sticker to each pair for that extra touch. '
                'One size fits most. Made from 75% Cotton, 23% Nylon, and 2% Spandex. The design shown is just one '
                'of many possibilities. Reach out to us to create your own unique custom sock today!'
            ],
            'priceExpiresDate': now,
            'ProductMarketingPointArray': {
                'ProductMarketingPoint': [
                    {
                        'pointType': 'Compliance',
                        'pointCopy': 'This product is Prop 65 compliant - no warning statement is required on '
                                     'this product.'
                    }
                ]
            },
            'ProductKeywordArray': None,
            'productBrand': None,
            'export': True,
            'ProductCategoryArray': {
                'ProductCategory': [
                    {
                        'category': 'Apparel',
                        'subCategory': None
                    },
                    {
                        'category': 'Socks',
                        'subCategory': None
                    },
                    {
                        'category': 'Custom',
                        'subCategory': None
                    },
                    {
                        'category': 'Custom Socks',
                        'subCategory': None
                    },
                    {
                        'category': 'Golf',
                        'subCategory': None
                    }
                ]
            },
            'RelatedProductArray': None,
            'primaryImageUrl': 'https://media.snugzusa.com/m/5e7b327f9d9e7d64/webimage-SK800D.png',
            'ProductPriceGroupArray': {
                'ProductPriceGroup': [
                    {
                        'ProductPriceArray': {
                            'ProductPrice': [
                                {
                                    'quantityMin': 250,
                                    'quantityMax': 499,
                                    'price': Decimal('10.12'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 500,
                                    'quantityMax': 999,
                                    'price': Decimal('9.20'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 1000,
                                    'quantityMax': 2499,
                                    'price': Decimal('9.00'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 2500,
                                    'quantityMax': 4999,
                                    'price': Decimal('8.67'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 5000,
                                    'quantityMax': 10000,
                                    'price': Decimal('8.58'),
                                    'discountCode': 'C'
                                }
                            ]
                        },
                        'groupName': 'Active',
                        'currency': 'USD',
                        'description': 'Active'
                    }
                ]
            },
            'complianceInfoAvailable': None,
            'unspscCommodityCode': 0,
            'LocationDecorationArray': {
                'LocationDecoration': [
                    {
                        'locationName': 'Belly Band Full Color Full Bleed',
                        'maxImprintColors': 0,
                        'decorationName': 'Full Color Label',
                        'locationDecorationComboDefault': False,
                        'priceIncludes': False
                    },
                    {
                        'locationName': 'Header Card Full Color Full Bleed',
                        'maxImprintColors': 0,
                        'decorationName': 'Full Color Label',
                        'locationDecorationComboDefault': False,
                        'priceIncludes': False
                    },
                    {
                        'locationName': 'Full Color Full Exterior',
                        'maxImprintColors': 24,
                        'decorationName': 'Dye-Sublimated',
                        'locationDecorationComboDefault': True,
                        'priceIncludes': True
                    }
                ]
            },
            'ProductPartArray': {
                'ProductPart': [
                    {
                        'partId': 'SK800D',
                        'primaryColor': None,
                        'description': [
                            'IMPORT Custom Digital Sublimation Crew Socks'
                        ],
                        'countryOfOrigin': 'CN',
                        'ColorArray': None,
                        'primaryMaterial': None,
                        'SpecificationArray': None,
                        'shape': None,
                        'ApparelSize': None,
                        'Dimension': {
                            'dimensionUom': 'IN',
                            'depth': None,
                            'height': None,
                            'width': None,
                            'weightUom': 'LB',
                            'weight': Decimal('0.1250000000')
                        },
                        'leadTime': 20,
                        'unspsc': None,
                        'gtin': None,
                        'isRushService': False,
                        'ProductPackagingArray': None,
                        'ShippingPackageArray': {
                            'ShippingPackage': [
                                {
                                    'packageType': 'Box',
                                    'description': None,
                                    'quantity': Decimal('200.0'),
                                    'dimensionUom': 'IN',
                                    'depth': Decimal('20.000'),
                                    'height': Decimal('9.000'),
                                    'width': Decimal('18.000'),
                                    'weightUom': 'LB',
                                    'weight': Decimal('25.0000000000')
                                }
                            ]
                        },
                        'endDate': None,
                        'effectiveDate': None,
                        'isCloseout': False,
                        'isCaution': False,
                        'cautionComment': None,
                        'nmfcCode': None,
                        'nmfcDescription': None,
                        'nmfcNumber': None,
                        'isOnDemand': True,
                        'isHazmat': False
                    }
                ]
            },
            'lastChangeDate': now,
            'creationDate': now,
            'endDate': None,
            'effectiveDate': None,
            'isCaution': False,
            'cautionComment': None,
            'isCloseout': None,
            'lineName': None,
            'defaultSetupCharge': None,
            'defaultRunCharge': None,
            'imprintSize': None,
            'FobPointArray': {
                'FobPoint': [
                    {
                        'fobId': '5',
                        'fobCity': None,
                        'fobState': 'China',
                        'fobPostalCode': 'Direct',
                        'fobCountry': 'US'
                    }
                ]
            }
        },
        'ServiceMessageArray': None
    }
    resp = ProductResponseV200.model_validate(data)
    assert resp.Product.productId == 'SK800D'
    assert resp.Product.FobPointArray.FobPoint[0].fobCity is None


def test_gold():
    now = datetime.now()
    data = {
        'Product': {
            'productId': 'TWIST',
            'productName': '14 Oz Stainless Tumbler With Polypropylene Liner',
            'description': [
                '14 Oz Stainless Tumbler With Polypropylene Liner'
            ],
            'ProductMarketingPointArray': None,
            'ProductKeywordArray': {
                'ProductKeyword': [
                    {
                        'keyword': 'Bpa Free'
                    },
                    {
                        'keyword': 'Tumbler'
                    },
                    {
                        'keyword': 'Travel Mug'
                    },
                    {
                        'keyword': 'Stainless'
                    },
                    {
                        'keyword': '14Oz'
                    },
                    {
                        'keyword': '14 Oz'
                    },
                    {
                        'keyword': 'Stainless Tumbler'
                    },
                    {
                        'keyword': 'Twist'
                    },
                    {
                        'keyword': 'Traveling'
                    },
                    {
                        'keyword': 'To-Go'
                    },
                    {
                        'keyword': 'Drinkware'
                    },
                    {
                        'keyword': 'Coffee'
                    }
                ]
            },
            'productBrand': None,
            'export': False,
            'ProductCategoryArray': {
                'ProductCategory': [
                    {
                        'category': 'Icons',
                        'subCategory': 'BPA Free'
                    },
                    {
                        'category': 'Stainless Tumblers',
                        'subCategory': None
                    }
                ]
            },
            'RelatedProductArray': None,
            'primaryImageUrl': 'http://s7d7.scene7.com/is/image/Goldbond/TWIST_GROUP?wid=500&hei=500&resMode=sharp&fmt=png-alpha',  # noqa
            # noqa
            'ProductPriceGroupArray': {
                'ProductPriceGroup': [
                    {
                        'ProductPriceArray': {
                            'ProductPrice': [
                                {
                                    'quantityMin': 0,
                                    'quantityMax': 50,
                                    'price': Decimal('10.75'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 50,
                                    'quantityMax': 100,
                                    'price': Decimal('10.75'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 100,
                                    'quantityMax': 200,
                                    'price': Decimal('10.35'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 200,
                                    'quantityMax': 400,
                                    'price': Decimal('9.95'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 400,
                                    'quantityMax': 800,
                                    'price': Decimal('9.55'),
                                    'discountCode': 'C'
                                },
                                {
                                    'quantityMin': 800,
                                    'quantityMax': 99999999,
                                    'price': Decimal('9.15'),
                                    'discountCode': 'C'
                                }
                            ]
                        },
                        'groupName': 'Net Pricing',
                        'currency': 'USD',
                        'description': 'Net Pricing'
                    }
                ]
            },
            'complianceInfoAvailable': None,
            'unspscCommodityCode': None,
            'LocationDecorationArray': {
                'LocationDecoration': [
                    {
                        'locationName': 'No Imprint',
                        'decorationName': None,
                        'locationDecorationComboDefault': None,
                        'priceIncludes': None,
                    },
                    {
                        'locationName': 'Panel',
                        'decorationName': None,
                        'locationDecorationComboDefault': None,
                        'priceIncludes': None
                    },
                    {
                        'locationName': '2 Sided',
                        'decorationName': None,
                        'locationDecorationComboDefault': None,
                        'priceIncludes': None
                    }
                ]
            },
            'ProductPartArray': {
                'ProductPart': [
                    {
                        'partId': 'TWIST-BDBK',
                        'primaryColor': None,
                        'description': [
                            '14 Oz Stainless Tumbler With Polypropylene Liner-Body Black'
                        ],
                        'countryOfOrigin': 'CN',
                        'ColorArray': {
                            'Color': [
                                {
                                    'standardColorName': None,
                                    'hex': '2D2926',
                                    'approximatePms': 'Black C',
                                    'colorName': 'Body Black'
                                }
                            ]
                        },
                        'primaryMaterial': None,
                        'SpecificationArray': None,
                        'shape': None,
                        'ApparelSize': None,
                        'Dimension': None,
                        'leadTime': None,
                        'unspsc': None,
                        'gtin': None,
                        'isRushService': False,
                        'ProductPackagingArray': None,
                        'ShippingPackageArray': {
                            'ShippingPackage': [
                                {
                                    'packageType': 'TWIST',
                                    'description': 'TWIST',
                                    'quantity': Decimal('25'),
                                    'dimensionUom': 'IN',
                                    'depth': Decimal('19'),
                                    'height': Decimal('6'),
                                    'width': Decimal('19'),
                                    'weightUom': 'LB',
                                    'weight': Decimal('1.85')
                                }
                            ]
                        },
                        'endDate': None,
                        'effectiveDate': None,
                        'isCloseout': False,
                        'isCaution': False,
                        'cautionComment': None,
                        'nmfcCode': None,
                        'nmfcDescription': None,
                        'nmfcNumber': None,
                        'isOnDemand': None,
                        'isHazmat': None
                    },
                    {
                        'partId': 'TWIST-BDWH',
                        'primaryColor': None,
                        'description': [
                            '14 Oz Stainless Tumbler With Polypropylene Liner-Body White'
                        ],
                        'countryOfOrigin': 'CN',
                        'ColorArray': {
                            'Color': [
                                {
                                    'standardColorName': None,
                                    'hex': 'FFFFFF',
                                    'approximatePms': 'White',
                                    'colorName': 'Body White'
                                }
                            ]
                        },
                        'primaryMaterial': None,
                        'SpecificationArray': None,
                        'shape': None,
                        'ApparelSize': None,
                        'Dimension': None,
                        'leadTime': None,
                        'unspsc': None,
                        'gtin': None,
                        'isRushService': False,
                        'ProductPackagingArray': None,
                        'ShippingPackageArray': {
                            'ShippingPackage': [
                                {
                                    'packageType': 'TWIST',
                                    'description': 'TWIST',
                                    'quantity': Decimal('25'),
                                    'dimensionUom': 'IN',
                                    'depth': Decimal('19'),
                                    'height': Decimal('6'),
                                    'width': Decimal('19'),
                                    'weightUom': 'LB',
                                    'weight': Decimal('1.85')
                                }
                            ]
                        },
                        'endDate': None,
                        'effectiveDate': None,
                        'isCloseout': False,
                        'isCaution': False,
                        'cautionComment': None,
                        'nmfcCode': None,
                        'nmfcDescription': None,
                        'nmfcNumber': None,
                        'isOnDemand': None,
                        'isHazmat': None
                    }
                ]
            },
            'lastChangeDate': now,
            'creationDate': now,
            'endDate': None,
            'effectiveDate': None,
            'isCaution': False,
            'cautionComment': None,
            'isCloseout': False,
            'lineName': None,
            'defaultSetupCharge': '40.00',
            'defaultRunCharge': None,
            'imprintSize': None,
            'FobPointArray': {
                'FobPoint': [
                    {
                        'fobId': '1',
                        'fobCity': 'Hixson',
                        'fobState': 'TN',
                        'fobPostalCode': '37343',
                        'fobCountry': 'US'
                    }
                ]
            }
        },
        'ServiceMessageArray': None
    }

    resp = ProductResponseV200.model_validate(data)
    assert resp.Product.productId == 'TWIST'
