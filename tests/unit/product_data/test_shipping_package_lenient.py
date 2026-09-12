"""Suppliers omit values the spec marks required; the API must not reject the whole product.

2026-09-12: every Aakron product failed at PSRESTful with "ShippingPackage.packageType: Input should be
a valid string" because Aakron sends packageType = null for each part.
"""
from decimal import Decimal

from psdomain.model.product_data.common import ShippingPackage, ShippingPackageArray


def _package(package_type):
    return {
        'packageType': package_type, 'description': None, 'quantity': Decimal('200'),
        'dimensionUom': 'IN', 'depth': Decimal('20'), 'height': Decimal('9'), 'width': Decimal('18'),
        'weightUom': 'LB', 'weight': Decimal('25'),
    }


def test_null_package_type_is_accepted():
    package = ShippingPackage.model_validate(_package(None))
    assert package.packageType is None
    assert package.quantity == Decimal('200')


def test_package_type_still_round_trips():
    arr = ShippingPackageArray.model_validate({'ShippingPackage': [_package('Box'), _package(None)]})
    assert [p.packageType for p in arr.ShippingPackage] == ['Box', None]
