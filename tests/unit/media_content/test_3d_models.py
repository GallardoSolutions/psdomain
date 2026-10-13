"""3D models sent as mediaType Image.

SanMar sends .glb files (glTF binary) with mediaType 'Image' and its custom class type 505 "Image 3D", e.g.
https://docs.companycasuals.com/productmedia/3d/BC3655_WhiteSlub.glb. They are not pictures: they can't be
rendered in an <img>, sized or classified, so they must never count as displayable images.
"""
import pytest

from psdomain.model.media_content import ClassType, ClassTypeArray, MediaContent, MODEL_3D_EXTENSIONS, PRIMARY


def _mc(url, class_types=(), media_type='Image'):
    return MediaContent(productId='BC3655', url=url, mediaType=media_type, singlePart=True,
                        ClassTypeArray=ClassTypeArray(ClassType=list(class_types)),
                        DecorationArray=None, LocationArray=None)


IMAGE_3D = ClassType(classTypeId=505, classTypeName='Image 3D')  # SanMar's custom class type


@pytest.mark.parametrize('url', [
    'https://docs.companycasuals.com/productmedia/3d/BC3655_WhiteSlub.glb',
    'https://cdn.example.com/models/mug.GLB',
    'https://cdn.example.com/models/mug.gltf',
    'https://cdn.example.com/models/mug.usdz',
    'https://cdn.example.com/models/mug.glb?v=3',
])
def test_3d_files_are_models_not_displayable_images(url):
    mc = _mc(url)
    assert mc.is_3d_model
    assert mc.is_image, 'still mediaType Image, as the supplier sent it'
    assert not mc.is_displayable


def test_3d_class_type_marks_an_extensionless_url():
    mc = _mc('https://cdn.example.com/assets/8f2c1a', class_types=[IMAGE_3D])
    assert mc.is_3d_model
    assert not mc.is_displayable


@pytest.mark.parametrize('name', ['Image 3D', '3D Model', 'image3d'])
def test_class_type_names_mentioning_3d(name):
    mc = _mc('https://cdn.example.com/assets/8f2c1a', class_types=[ClassType(classTypeId=777, classTypeName=name)])
    assert mc.is_3d_model


@pytest.mark.parametrize('url', [
    'https://cdn.example.com/BC3655_WhiteSlub.jpg',
    'https://cdn.example.com/3d/BC3655_WhiteSlub.png',  # a "3d" folder alone doesn't make it a model
    'https://cdn.example.com/assets/8f2c1a',
    None,
])
def test_pictures_are_not_models(url):
    mc = _mc(url, class_types=[ClassType(classTypeId=PRIMARY, classTypeName='Primary')])
    assert not mc.is_3d_model


def test_a_picture_is_still_displayable():
    assert _mc('https://cdn.example.com/BC3655_WhiteSlub.jpg').is_displayable


def test_known_extensions():
    assert {'.glb', '.gltf', '.usdz'} <= set(MODEL_3D_EXTENSIONS)
