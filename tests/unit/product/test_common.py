from psdomain.model.product_data.common import FobPoint


def test_fob_city_can_be_none():
    data = {
        'fobId': '5',
        'fobCity': None,
        'fobState': 'China',
        'fobPostalCode': 'Direct',
        'fobCountry': 'US'
    }
    fob_point = FobPoint.model_validate(data)
    assert fob_point.fobCity is None

