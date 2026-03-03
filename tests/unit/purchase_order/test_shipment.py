from psdomain.model.purchase_order import (
    ContactDetails,
    FreightDetails,
    ShipTo,
    Shipment,
)


def _make_ship_to(**overrides):
    defaults = dict(
        customerPickup=False,
        shipmentId=1,
        ContactDetails=ContactDetails(
            companyName="Acme Corp",
            address1="123 Main St",
            city="Springfield",
            region="IL",
            postalCode="62701",
            country="US",
        ),
    )
    defaults.update(overrides)
    return ShipTo(**defaults)


def test_shipment_without_freight_details():
    """FreightDetails is optional per the SOAP definition for SendPO."""
    shipment = Shipment(
        ShipTo=_make_ship_to(),
        packingListRequired=True,
        blindShip=False,
        allowConsolidation=False,
    )
    assert shipment.FreightDetails is None


def test_shipment_with_freight_details():
    """FreightDetails can still be provided when needed."""
    shipment = Shipment(
        ShipTo=_make_ship_to(),
        packingListRequired=True,
        blindShip=False,
        allowConsolidation=False,
        FreightDetails=FreightDetails(carrier="UPS", service="GROUND"),
    )
    assert shipment.FreightDetails is not None
    assert shipment.FreightDetails.carrier == "UPS"
    assert shipment.FreightDetails.service == "GROUND"
