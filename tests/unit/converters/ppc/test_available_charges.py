"""
Tests for PPC AvailableCharges converter.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.ppc import (
    AvailableChargesResponse,
    AvailableCharge,
    AvailableChargeArray,
    ChargeType,
)
from psdomain.model.base import ErrorMessage
from psdomain.converters.ppc import available_charges


class TestAvailableChargesConverter:
    """Tests for PPC Available Charges converter."""

    def test_available_charges_response(self):
        """Test available charges response conversion."""
        charges = [
            AvailableCharge(
                chargeId=1,
                chargeName="Setup Charge",
                chargeType=ChargeType.SETUP,
                chargeDescription="Initial setup fee",
            ),
            AvailableCharge(
                chargeId=2,
                chargeName="Run Charge",
                chargeType=ChargeType.RUN,
                chargeDescription="Per item charge",
            ),
        ]

        response = AvailableChargesResponse(
            AvailableChargeArray=AvailableChargeArray(AvailableCharge=charges),
            ErrorMessage=None,
        )

        proto_response = available_charges.available_charges_to_proto(response)

        # Verify proto
        assert len(proto_response.charges) == 2
        assert proto_response.charges[0].charge_id == 1
        assert proto_response.charges[0].charge_name == "Setup Charge"
        assert proto_response.charges[0].charge_type == "Setup"

        # Roundtrip
        roundtrip = available_charges.available_charges_from_proto(proto_response)
        assert len(roundtrip.AvailableChargeArray.AvailableCharge) == 2
        assert roundtrip.AvailableChargeArray.AvailableCharge[0].chargeType == ChargeType.SETUP

    def test_available_charges_order_type(self):
        """Test available charges with Order charge type."""
        charges = [
            AvailableCharge(
                chargeId=3,
                chargeName="Order Charge",
                chargeType=ChargeType.ORDER,
                chargeDescription="Per order fee",
            ),
        ]

        response = AvailableChargesResponse(
            AvailableChargeArray=AvailableChargeArray(AvailableCharge=charges),
            ErrorMessage=None,
        )

        proto_response = available_charges.available_charges_to_proto(response)

        # Verify proto
        assert proto_response.charges[0].charge_type == "Order"

        # Roundtrip
        roundtrip = available_charges.available_charges_from_proto(proto_response)
        assert roundtrip.AvailableChargeArray.AvailableCharge[0].chargeType == ChargeType.ORDER

    def test_available_charges_with_error(self):
        """Test available charges response with error message."""
        response = AvailableChargesResponse(
            AvailableChargeArray=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = available_charges.available_charges_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404

        # Roundtrip
        roundtrip = available_charges.available_charges_from_proto(proto_response)
        assert roundtrip.AvailableChargeArray is None
        assert roundtrip.ErrorMessage.code == 404
