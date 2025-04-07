# flake8: noqa F811
from psdomain.model import DecorationColorResponse
from .fixtures import decoration_colors_ok  # noqa
from .responses.decoration_colors import decoration_colors_response_pms_match_and_full_color_null


def test_colors(decoration_colors_ok):
    resp = decoration_colors_ok
    assert resp.ErrorMessage is None
    colors = resp.colors
    assert len(colors) == 1
    color = colors[0]
    assert color.colorName == 'Standard'
    assert color.hex is None
    assert color.approximatePms is None
    assert color.standardColorName is None


def test_decoration_methods(decoration_colors_ok):
    resp = decoration_colors_ok
    #
    decoration_methods = resp.decoration_methods
    assert len(decoration_methods) == 2
    decoration_method = decoration_methods[0]
    assert decoration_method.decorationId == 1
    assert decoration_method.decorationName == 'Embroidery'
    decoration_method = decoration_methods[1]
    assert decoration_method.decorationId == 2
    assert decoration_method.decorationName == 'Imprinted'


def test_decoration_colors_pms_match_and_full_color_null():
    # although the documentation says that pmsMatch and fullColor are required boolean values,
    # the wsdl says they are optional and can be null
    resp = DecorationColorResponse.model_validate(decoration_colors_response_pms_match_and_full_color_null)
    assert resp.ErrorMessage is None
    assert resp.DecorationColors.pmsMatch is None
    assert resp.DecorationColors.fullColor is None
    response = {
        'DecorationColors': {
            'ColorArray': {
                'Color': [
                    {
                        'colorId': '563',
                        'colorName': 'CMYK'
                    }
                ]
            },
            'productId': 'AM01',
            'locationId': 16986,
            'DecorationMethodArray': {
                'DecorationMethod': [
                    {
                        'decorationId': 115,
                        'decorationName': '4 Color'
                    }
                ]
            },
            'pmsMatch': None,
            'fullColor': None
        },
        'ErrorMessage': None
    }
    resp = DecorationColorResponse.model_validate(response)
    assert resp.DecorationColors.pmsMatch is None
    assert resp.DecorationColors.fullColor is None