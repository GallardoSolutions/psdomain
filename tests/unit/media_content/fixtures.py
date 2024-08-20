import pytest

from psdomain.model.media_content import MediaContent, MediaType, BLANK, ClassTypeArray

null, false, true = None, False, True


@pytest.fixture
def blank_mc():
    return MediaContent(
        productId='2703', partId=None, singlePart=True, fileSize=None, mediaType=MediaType.IMAGE,
        url='https://assets.pcna.com/t_PS_SMALL/Images/1220-93BK_B_FR.jpg',
        width=None, height=None, dpi=None, color=None, description=None, changeTimeStamp=None,
        ClassTypeArray=ClassTypeArray.from_class_types([BLANK]),
        DecorationArray=None, LocationArray=None
    )


@pytest.fixture
def blank_hit():
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
