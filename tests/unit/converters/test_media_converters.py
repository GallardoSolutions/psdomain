"""
Tests for media content converters (v110).

Tests roundtrip conversion: JSON -> Pydantic -> Proto -> Pydantic
"""
import pytest

from psdomain.model.media_content import (
    MediaContent,
    MediaType,
    BLANK,
    REAR,
    PRIMARY,
    ClassTypeArray,
    DecorationArray,
    Decoration,
)

null, false, true = None, False, True


@pytest.fixture
def blank_hit():
    """Fixture from tests/unit/media_content/fixtures.py"""
    data = {
        "productId": "55410",
        "partId": "5410SBLK",
        "url": "https://www.hitpromo.net/imageManager/show/55410_BLK_Back_Blank.jpg",
        "mediaType": "Image",
        "fileSize": null,
        "width": null,
        "height": null,
        "dpi": null,
        "color": null,
        "description": null,
        "singlePart": false,
        "changeTimeStamp": null,
        "ClassTypeArray": {
            "ClassType": [
                {
                    "classTypeId": 1008,
                    "classTypeName": "Rear"
                }
            ]
        },
        "DecorationArray": {
            "Decoration": [
                {
                    "decorationId": 51,
                    "decorationName": "Blank"
                }
            ]
        },
        "LocationArray": null
    }
    return MediaContent.model_validate(data)


@pytest.fixture
def primary_decorated():
    """Fixture from tests/unit/media_content/fixtures.py"""
    data = {
        "productId": "55410",
        "partId": "5410SBLK",
        "url": "https://www.hitpromo.net/imageManager/show/55410_BLK_Laser.jpg",
        "mediaType": "Image",
        "fileSize": null,
        "width": null,
        "height": null,
        "dpi": null,
        "color": null,
        "description": null,
        "singlePart": false,
        "changeTimeStamp": null,
        "ClassTypeArray": {
            "ClassType": [
                {
                    "classTypeId": 1006,
                    "classTypeName": "Primary"
                }
            ]
        },
        "DecorationArray": {
            "Decoration": [
                {
                    "decorationId": 58,
                    "decorationName": "Laser Engraving"
                }
            ]
        },
        "LocationArray": null
    }
    return MediaContent.model_validate(data)


@pytest.fixture
def media_with_location():
    """MediaContent with location information."""
    data = {
        "productId": "LOC-001",
        "partId": "LOC-PART",
        "url": "https://example.com/image.jpg",
        "mediaType": "Image",
        "fileSize": 1024.0,
        "width": 800,
        "height": 600,
        "dpi": 72,
        "color": "Red",
        "description": "Product front view",
        "singlePart": true,
        "changeTimeStamp": null,
        "ClassTypeArray": {
            "ClassType": [
                {"classTypeId": 1001, "classTypeName": "Blank"},
                {"classTypeId": 1007, "classTypeName": "Front"}
            ]
        },
        "DecorationArray": {
            "Decoration": [
                {"decorationId": 1, "decorationName": "Screen Print"},
                {"decorationId": 2, "decorationName": "Embroidery"}
            ]
        },
        "LocationArray": {
            "Location": [
                {"locationId": 100, "locationName": "Front Center"},
                {"locationId": 101, "locationName": "Back Center"}
            ]
        }
    }
    return MediaContent.model_validate(data)


class TestMediaV110Converter:
    """Tests for Media Content v1.1.0 converter."""

    def test_blank_hit_to_proto(self, blank_hit):
        """Test conversion of blank_hit fixture to proto.

        This test verifies that ClassTypeArray and DecorationArray
        are properly converted to proto repeated fields.
        """
        from psdomain.converters.media import v110

        # Convert to proto
        proto_mc = v110.media_content_to_proto(blank_hit)

        # Verify basic fields
        assert proto_mc.product_id == "55410"
        assert proto_mc.part_id == "5410SBLK"
        assert proto_mc.url == "https://www.hitpromo.net/imageManager/show/55410_BLK_Back_Blank.jpg"
        assert proto_mc.media_type == "Image"
        assert proto_mc.single_part is False

        # Verify ClassTypeArray was converted to class_types
        assert len(proto_mc.class_types) == 1
        assert proto_mc.class_types[0].class_type_id == 1008
        assert proto_mc.class_types[0].class_type_name == "Rear"

        # Verify DecorationArray was converted to decorations
        assert len(proto_mc.decorations) == 1
        assert proto_mc.decorations[0].decoration_id == 51
        assert proto_mc.decorations[0].decoration_name == "Blank"

    def test_blank_hit_roundtrip(self, blank_hit):
        """Test roundtrip conversion of blank_hit fixture."""
        from psdomain.converters.media import v110

        # Convert to proto and back
        proto_mc = v110.media_content_to_proto(blank_hit)
        roundtrip = v110.media_content_from_proto(proto_mc)

        # Verify basic fields
        assert roundtrip.productId == blank_hit.productId
        assert roundtrip.partId == blank_hit.partId
        assert roundtrip.url == blank_hit.url
        assert roundtrip.mediaType == blank_hit.mediaType
        assert roundtrip.singlePart == blank_hit.singlePart

        # Verify ClassTypeArray was preserved
        assert len(roundtrip.ClassTypeArray.ClassType) == 1
        assert roundtrip.ClassTypeArray.ClassType[0].classTypeId == 1008
        assert roundtrip.ClassTypeArray.ClassType[0].classTypeName == "Rear"

        # Verify DecorationArray was preserved
        assert roundtrip.DecorationArray is not None
        assert len(roundtrip.DecorationArray.Decoration) == 1
        assert roundtrip.DecorationArray.Decoration[0].decorationId == 51
        assert roundtrip.DecorationArray.Decoration[0].decorationName == "Blank"

    def test_primary_decorated_to_proto(self, primary_decorated):
        """Test conversion of primary_decorated fixture to proto."""
        from psdomain.converters.media import v110

        proto_mc = v110.media_content_to_proto(primary_decorated)

        # Verify ClassTypeArray
        assert len(proto_mc.class_types) == 1
        assert proto_mc.class_types[0].class_type_id == 1006
        assert proto_mc.class_types[0].class_type_name == "Primary"

        # Verify DecorationArray
        assert len(proto_mc.decorations) == 1
        assert proto_mc.decorations[0].decoration_id == 58
        assert proto_mc.decorations[0].decoration_name == "Laser Engraving"

    def test_media_with_multiple_class_types_and_decorations(self, media_with_location):
        """Test conversion with multiple class types, decorations, and locations."""
        from psdomain.converters.media import v110

        proto_mc = v110.media_content_to_proto(media_with_location)

        # Verify multiple class types
        assert len(proto_mc.class_types) == 2
        class_type_ids = {ct.class_type_id for ct in proto_mc.class_types}
        assert class_type_ids == {1001, 1007}

        # Verify multiple decorations
        assert len(proto_mc.decorations) == 2
        decoration_ids = {d.decoration_id for d in proto_mc.decorations}
        assert decoration_ids == {1, 2}

        # Verify multiple locations
        assert len(proto_mc.locations) == 2
        location_ids = {loc.location_id for loc in proto_mc.locations}
        assert location_ids == {100, 101}

    def test_media_with_location_roundtrip(self, media_with_location):
        """Test roundtrip conversion preserves all nested arrays."""
        from psdomain.converters.media import v110

        proto_mc = v110.media_content_to_proto(media_with_location)
        roundtrip = v110.media_content_from_proto(proto_mc)

        # Verify basic fields
        assert roundtrip.productId == "LOC-001"
        assert roundtrip.partId == "LOC-PART"
        assert roundtrip.width == 800
        assert roundtrip.height == 600
        assert roundtrip.dpi == 72
        assert roundtrip.color == "Red"
        assert roundtrip.description == "Product front view"
        assert roundtrip.singlePart is True

        # Verify ClassTypeArray
        assert len(roundtrip.ClassTypeArray.ClassType) == 2
        class_type_ids = {ct.classTypeId for ct in roundtrip.ClassTypeArray.ClassType}
        assert class_type_ids == {1001, 1007}

        # Verify DecorationArray
        assert roundtrip.DecorationArray is not None
        assert len(roundtrip.DecorationArray.Decoration) == 2
        decoration_ids = {d.decorationId for d in roundtrip.DecorationArray.Decoration}
        assert decoration_ids == {1, 2}

        # Verify LocationArray
        assert roundtrip.LocationArray is not None
        assert len(roundtrip.LocationArray.Location) == 2
        location_ids = {loc.locationId for loc in roundtrip.LocationArray.Location}
        assert location_ids == {100, 101}

    def test_media_content_with_null_arrays(self):
        """Test conversion when DecorationArray and LocationArray are None."""
        from psdomain.converters.media import v110

        data = {
            "productId": "NULL-001",
            "partId": None,
            "url": "https://example.com/image.jpg",
            "mediaType": "Image",
            "fileSize": None,
            "width": None,
            "height": None,
            "dpi": None,
            "color": None,
            "description": None,
            "singlePart": True,
            "changeTimeStamp": None,
            "ClassTypeArray": {
                "ClassType": [
                    {"classTypeId": 1001, "classTypeName": "Blank"}
                ]
            },
            "DecorationArray": None,
            "LocationArray": None
        }
        mc = MediaContent.model_validate(data)

        proto_mc = v110.media_content_to_proto(mc)

        # Basic fields
        assert proto_mc.product_id == "NULL-001"
        assert proto_mc.single_part is True

        # ClassTypeArray should still be converted
        assert len(proto_mc.class_types) == 1

        # Empty repeated fields for null arrays
        assert len(proto_mc.decorations) == 0
        assert len(proto_mc.locations) == 0

        # Roundtrip
        roundtrip = v110.media_content_from_proto(proto_mc)
        assert roundtrip.productId == "NULL-001"
        assert roundtrip.DecorationArray is None or len(roundtrip.DecorationArray.Decoration) == 0
        assert roundtrip.LocationArray is None or len(roundtrip.LocationArray.Location) == 0
