# flake8: noqa F811

from .fixtures import decoration_colors_ok  # noqa


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
