from psdomain.utils.text import slugify


def test_slugify():
    name = 'Cap America Premium Trucker Mesh Back Cap'
    product_id = 'SM-8408'
    full_name = f'{name}-{product_id}'
    assert slugify(full_name) == 'cap-america-premium-trucker-mesh-back-cap-sm-8408'
    #
    text = "Hello, World! This is a test."
    assert slugify(text) == "hello-world-this-is-a-test"
