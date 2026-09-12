"""A null entry inside ColorArray.Color must not reject the whole product.

2026-09-12: EVANS product 1974 answers ``"ColorArray": {"Color": [null]}`` on one part, and PSRESTful
returned HTTP 400 for the product on every PromoSync import attempt (PROMOSYNC-67, 85 events).
"""
from psdomain.model.product_data.common import ColorArray


def test_null_entries_are_dropped():
    arr = ColorArray.model_validate({'Color': [None, {'colorName': 'Red'}, None]})
    assert [c.colorName for c in arr.Color] == ['Red']


def test_only_null_entries_gives_an_empty_list():
    assert ColorArray.model_validate({'Color': [None]}).Color == []


def test_missing_list_is_still_required():
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ColorArray.model_validate({})
