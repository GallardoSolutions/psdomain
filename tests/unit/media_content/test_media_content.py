# flake8: noqa F811
import pytest
from pydantic import ValidationError
from .fixtures import blank_mc, blank_hit, primary_decorated  # noqa
from psdomain.model.media_content import ClassType, ClassTypeArray, BLANK, FRONT, DECORATED, DecorationArray, \
    Decoration, Location, LocationArray, MediaContent, MediaContentArray, MediaContentDetailsResponse  # noqa


def test_is_blank(blank_mc, blank_hit):
    assert blank_mc.is_blank
    assert blank_hit.is_blank


def test_is_primary(primary_decorated):
    assert primary_decorated.is_primary


def test_is_decorated(blank_mc, blank_hit, primary_decorated):
    assert not blank_mc.is_decorated
    assert not blank_hit.is_decorated
    assert primary_decorated.is_decorated


def test_is_group(blank_mc, primary_decorated):
    assert not blank_mc.is_group
    assert primary_decorated.is_group  # although the image is really a single part(HIT classification issue)


def test_from_class_type_id():
    blank = ClassType.from_class_type_id(BLANK)
    assert blank.is_blank


def test_from_class_type_ids():
    blank_front_arr = ClassTypeArray.from_class_types([BLANK, FRONT])
    class_type_ids = blank_front_arr.get_class_types()
    assert BLANK in class_type_ids
    assert FRONT in class_type_ids
    assert DECORATED not in class_type_ids
    assert blank_front_arr.names_list == ['Blank', 'Front']


def test_location_list():
    lst = [
        Location(locationId=23, locationName='Side'),
        Location(locationId=45, locationName='Back')
    ]
    arr = LocationArray(Location=lst)
    names_list = arr.names_list
    assert names_list == ['Side', 'Back']


def test_location_name_optional_id_required():
    # locationName is optional (minOccurs=0); locationId is required (minOccurs=1).
    loc = Location(locationId=23)
    assert loc.locationId == 23
    assert loc.locationName is None
    with pytest.raises(ValidationError):
        Location(locationName='Side')


def test_location_array_names_list_skips_none():
    arr = LocationArray(Location=[
        Location(locationId=23, locationName='Side'),
        Location(locationId=24),
    ])
    assert arr.names_list == ['Side']
    assert arr.names == 'Side'


def test_decoration_list():
    lst = [
        Decoration(decorationId=10, decorationName='Screen Print'),
        Decoration(decorationId=11, decorationName='Embroidery'),
    ]
    arr = DecorationArray(Decoration=lst)
    names_list = arr.names_list
    assert names_list == ['Screen Print', 'Embroidery']


def test_decoration_allows_none_id():
    # Bel Promo returns a 'Blank' decoration with no decorationId.
    dec = Decoration(decorationName='Blank')
    assert dec.decorationId is None
    assert dec.decorationName == 'Blank'
    assert dec.is_blank


def test_decoration_allows_both_none():
    # The MediaContent 1.1.0 SOAP definition allows both fields to be absent.
    dec = Decoration()
    assert dec.decorationId is None
    assert dec.decorationName is None
    assert not dec.is_blank


def test_decoration_array_names_list_skips_none():
    lst = [
        Decoration(decorationId=1, decorationName='screen_print'),
        Decoration(decorationName='Blank'),
        Decoration(),
    ]
    arr = DecorationArray(Decoration=lst)
    assert arr.names_list == ['screen_print', 'Blank']
    assert arr.names == 'screen_print, Blank'


def test_media_content_with_blank_decoration_no_id():
    # Reproduces the Bel Promo proto message: a 'Blank' decoration without decorationId.
    data = {
        "productId": "A0024AL",
        "partId": "A0024AL-Clear",
        "url": "https://belusaweb.s3.amazonaws.com/product-images/designlab/clear.jpg",
        "mediaType": "Image",
        "singlePart": True,
        "ClassTypeArray": {
            "ClassType": [
                {"classTypeId": 1006, "classTypeName": "Primary"},
                {"classTypeId": 2000, "classTypeName": "Standard"},
            ]
        },
        "DecorationArray": {
            "Decoration": [
                {"decorationName": "Blank"}
            ]
        },
        "LocationArray": None,
    }
    mc = MediaContent.model_validate(data)
    assert mc.decorations[0].decorationId is None
    assert mc.decorations[0].is_blank
    assert mc.is_blank
    assert not mc.is_decorated


def test_get_unique_urls():
    # test MediaContentDetailsResponse.get_unique_urls
    empty_class_type_arr = ClassTypeArray(ClassType=[])
    lst = [
        MediaContent(url='http://www.example.com/1',
                     mediaType='Image', productId='2',
                     ClassTypeArray=empty_class_type_arr, DecorationArray=None, LocationArray=None,
                     singlePart=True),
        MediaContent(url='http://www.example.com/2',
                     mediaType='Image', productId='2',
                     ClassTypeArray=empty_class_type_arr, DecorationArray=None, LocationArray=None,
                     singlePart=True
                     ),
        MediaContent(url='http://www.example.com/1',
                     mediaType='Image', productId='2',
                     ClassTypeArray=empty_class_type_arr, DecorationArray=None, LocationArray=None,
                     singlePart=True
                     ),
    ]
    arr = MediaContentArray(MediaContent=lst)
    response = MediaContentDetailsResponse(MediaContentArray=arr, errorMessage=None)
    unique_urls = response.get_unique_urls()
    assert unique_urls == {'http://www.example.com/1', 'http://www.example.com/2'}


def test_is_displayable():
    img_prefix = 'http://www.example.com/'
    core_dict = dict(productId='2',
                     ClassTypeArray=ClassTypeArray(ClassType=[]),
                     DecorationArray=None,
                     LocationArray=None,
                     singlePart=True)
    # Non Image are not displayable
    for mt in ('Video', 'Audio', 'Document'):
        mc = MediaContent(url=f'{img_prefix}/1',
                          mediaType=mt,
                          **core_dict)
        assert not mc.is_displayable
    # Image are displayable
    mc = MediaContent(url=f'{img_prefix}/1',
                      mediaType='Image',
                      **core_dict)
    assert mc.is_displayable
    # Image with no URL are not displayable
    mc = MediaContent(url=None,
                      mediaType='Image',
                      **core_dict)
    assert not mc.is_displayable
    # pdfs and psds are not displayable
    for ext in ('pdf', 'psd', 'PSD', 'PDF'):
        mc = MediaContent(url=f'{img_prefix}/1.{ext}',
                          mediaType='Image',
                          **core_dict)
        assert not mc.is_displayable
    # jpgs, pngs, gifs are displayable
    for ext in ('jpg', 'png', 'gif', 'JPG', 'PNG', 'GIF'):
        mc = MediaContent(url=f'{img_prefix}/1.{ext}',
                          mediaType='Image',
                          **core_dict)
        assert mc.is_displayable


def test_is_too_big():
    img_prefix = 'https://www.example.com/'
    core_dict = dict(productId='2',
                     ClassTypeArray=ClassTypeArray(ClassType=[]),
                     DecorationArray=None,
                     LocationArray=None,
                     singlePart=True)
    # if no filesize, no height, or no with, it is not too big
    mc = MediaContent(url=f'{img_prefix}/1',
                      mediaType='Image',
                      **core_dict)
    assert not mc.is_too_big
