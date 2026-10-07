"""Extended class types (8000+), outside the PromoStandards range."""
from psdomain.model.media_content import (
    ClassType, ClassTypeArray, MediaContent, BLANK, FRONT, PRIMARY,
    HIGH_RESOLUTION, MODEL, LIFESTYLE, CUSTOM_CLASS_TYPES,
)


def _mc(class_types):
    return MediaContent(productId='P1', url='https://cdn/x.jpg', mediaType='Image', singlePart=True,
                        ClassTypeArray=ClassTypeArray.from_class_types(class_types),
                        DecorationArray=None, LocationArray=None)


def test_extended_ids():
    assert (HIGH_RESOLUTION, MODEL, LIFESTYLE) == (8000, 8001, 8002)
    assert CUSTOM_CLASS_TYPES == frozenset({8000, 8001, 8002})


def test_names_are_not_custom():
    assert ClassType.from_class_type_id(HIGH_RESOLUTION).classTypeName == 'High Resolution'
    assert ClassType.from_class_type_id(MODEL).classTypeName == 'Model'
    assert ClassType.from_class_type_id(LIFESTYLE).classTypeName == 'Lifestyle'


def test_model_and_lifestyle_flags():
    model_front = _mc([BLANK, MODEL, FRONT, PRIMARY])
    assert model_front.is_model and model_front.is_front and not model_front.is_lifestyle
    lifestyle = _mc([LIFESTYLE])
    assert lifestyle.is_lifestyle and not lifestyle.is_model
    flat_front = _mc([BLANK, FRONT])
    assert not flat_front.is_model and not flat_front.is_lifestyle


def test_parses_payload_with_extended_class_types():
    # A model shot that also carries the standard Blank / Front / Primary class types.
    mc = MediaContent.model_validate({
        'productId': 'P1', 'url': 'https://cdn/p1_model_front.jpg', 'mediaType': 'Image',
        'singlePart': True, 'DecorationArray': None, 'LocationArray': None,
        'ClassTypeArray': {'ClassType': [
            {'classTypeId': 2001, 'classTypeName': 'High'}, {'classTypeId': 1001, 'classTypeName': 'Blank'},
            {'classTypeId': 8001, 'classTypeName': 'Model'}, {'classTypeId': 1007, 'classTypeName': 'Front'},
            {'classTypeId': 1006, 'classTypeName': 'Primary'}]},
    })
    assert mc.is_model and mc.is_primary and mc.is_front and mc.is_blank
