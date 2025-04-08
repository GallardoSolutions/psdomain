# flake8: noqa F811
from decimal import Decimal
from dataclasses import dataclass

from psdomain.model.product_data.v_2_0_0 import GetProductSellableResponseV200, ProductCloseOutResponseV200, \
    ProductDateModifiedResponseV200, ProductResponseV200
from psdomain.model.product_data.v_1_0_0 import ProductCloseOutResponseV100, ProductDateModifiedResponseV100, \
    GetProductSellableResponseV100, ProductResponseV100
from psdomain.model.base import Severity
from psdomain.model.product_data.common import ProductPartArray, sort_sizes, ProductCategory, Product, ApparelSize, \
    ProductCategoryArray, RelatedProductArray, ProductKeywordArray, ProductMarketingPointArray, RelatedProduct

from .responses.product_parts import product_part_array
from .fixtures import sellable_response, resp_alpha  # noqa


def test_get_product_sellable_response_v200(sellable_response):
    response = GetProductSellableResponseV200.model_validate(sellable_response)

    arr = response.ProductSellableArray.ProductSellable

    assert arr[0].productId == '0011-86'
    assert arr[0].partId == '0011-86BK'
    assert arr[0].culturePoint is None

    assert arr[1].productId == '0022-45'
    assert arr[1].partId == '0022-45BK'
    assert arr[1].culturePoint is None

    assert arr[2].productId == '0022-46'
    assert arr[2].partId == '0022-46BK'
    assert arr[2].culturePoint is None


def test_not_supported_v200():
    classes = [ProductResponseV200, ProductCloseOutResponseV200, ProductDateModifiedResponseV200,
               GetProductSellableResponseV200]
    for cls in classes:
        resp = cls.not_supported()
        assert resp.is_ok is False
        msg = resp.ServiceMessageArray.ServiceMessage[0]
        assert msg.code == 125
        assert msg.description == 'Not Supported'
        assert msg.severity == Severity.ERROR


def test_not_supported_v100():
    classes = [ProductResponseV100, ProductCloseOutResponseV100, ProductDateModifiedResponseV100,
               GetProductSellableResponseV100]
    for cls in classes:
        resp = cls.not_supported()
        assert resp.is_ok is False
        msg = resp.ErrorMessage
        assert msg.code == 125
        assert msg.description == 'Not Supported'


def test_sort_sizes():
    """
    Test sort_sizes function for product parts
    """
    product_parts = ProductPartArray.model_validate(product_part_array).ProductPart
    sorted_parts = sort_sizes(product_parts)
    for pp in sorted_parts[:8]:
        assert pp.get_size() == 'XS'
    for pp in sorted_parts[8:8 + 6]:
        assert pp.get_size() == 'S'
    for pp in sorted_parts[14:14 + 6]:
        assert pp.get_size() == 'M'
    for pp in sorted_parts[20:20 + 6]:
        assert pp.get_size() == 'L'
    for pp in sorted_parts[26:26 + 7]:
        assert pp.get_size() == 'XL'
    for pp in sorted_parts[33:33 + 7]:
        assert pp.get_size() == '2XL'


def test_html_description(resp_alpha):
    """
    Test html_description property for product
    """
    desc = resp_alpha.Product.get_html_description()
    want = "4.1 oz., 20 singles; 50% recycled polyester, 38% cotton, 12% rayon;Bound self neckband; Blind hem <br>" \
           "stitching detail on sleeves and bottom hem; Ladies' contemporary fit; Imperfectly knit to create <br>" \
           "vintage striations; A- list status from CDP (Carbon Disclosure Project); Energy Star Partner of the <br>" \
           "Year (14 consecutive years); Every piece of Alternative apparel purchased from our company qualifies <br>" \
           "for Hanes4Education;"
    assert desc == want


def test_is_on_demand(resp_alpha):
    """
    Test is_on_demand property for product
    """
    assert resp_alpha.Product.is_on_demand is False


def test_is_closeout(resp_alpha):
    """
    Test is_closeout property for product
    """
    assert resp_alpha.Product.is_closeout is False


def test_brand(resp_alpha):
    """
    Test brand property for product
    """
    assert resp_alpha.Product.brand == 'Alternative'


def test_get_min_qty(resp_alpha):
    """
    Test get_min_qty method for product
    """
    assert resp_alpha.Product.get_min_qty() == 1
    assert resp_alpha.Product.get_min_qty('USD', 'Blank') == 1


def test_categories(resp_alpha):
    """
    Test categories property for product
    """
    assert resp_alpha.Product.categories == 'T-Shirts'


def test_variants_per_color(resp_alpha):
    """
    Test variants_per_color property for product
    """
    variants = resp_alpha.Product.variants_per_color
    assert len(variants) > 0
    parts = variants['ECO BLACK']
    assert parts == ['B30924517', 'B30924516', 'B30924512']


def test_substitutes(resp_alpha):
    """
    Test substitutes property for product
    """
    substitutes = resp_alpha.Product.substitutes
    assert len(substitutes) > 0
    substitute_product_ids = {sub.productId for sub in substitutes}
    assert substitute_product_ids == {'AA1973', 'EC3800'}


def test_companion_sells(resp_alpha):
    """
    Test companion_sells property for product
    """
    companions = resp_alpha.Product.companions
    assert len(companions) == 0


def test_common_groups(resp_alpha):
    """
    Test common_groupings property for product
    """
    common = resp_alpha.Product.common_groupings
    assert len(common) == 0


def test_age_group(resp_alpha):
    """
    Test age_group property for product.ApparelSize
    """
    first_part = resp_alpha.Product.first_part
    assert first_part.ApparelSize.google_age_group == 'adult'


def test_google_gender(resp_alpha):
    """
    Test google_gender property for product.ApparelSize
    """
    first_part = resp_alpha.Product.first_part
    assert first_part.ApparelSize.google_gender == 'female'


def test_full_category():
    pc = ProductCategory(category='apparel', subCategory='t-shirts')
    assert pc.full_category == 'Apparel > T-Shirts'
    #
    pc.subCategory = '-'
    assert pc.full_category == 'Apparel'
    #
    pc = ProductCategory(category='Drinkware', subCategory='tumblers')
    assert pc.full_category == 'Drinkware > Tumblers'
    #
    product = Product(
        productId='1035', productName='Tumbler',
        ProductCategoryArray=ProductCategoryArray(ProductCategory=[pc]),
        ProductPartArray=ProductPartArray(ProductPart=[]),
        RelatedProductArray=RelatedProductArray(RelatedProduct=[]),
        ProductKeywordArray=ProductKeywordArray(ProductKeyword=[]),
        ProductMarketingPointArray=ProductMarketingPointArray(ProductMarketingPoint=[]),
    )
    assert product.main_category == 'Drinkware > Tumblers'


def test_get_list_price(resp_alpha):
    price = resp_alpha.Product.get_list_price()
    assert price == Decimal('23.10')


def test_relation_type():
    """
    <RelatedProduct>
        <relationType>You may also like</relationType>
        <productId>332222</productId>
        <partId />
    </RelatedProduct>
    :return:
    """
    data = {
        'relationType': 'You may also like',
        'productId': '332222',
        'partId': None
    }
    product = RelatedProduct(**data)
    assert product.is_substitute is True
    assert product.is_companion_sell is False
    assert product.is_common_grouping is False


def test_apparel_size_fallback():
    data = {
        'apparelStyle': 'Unisex',
        'labelSize': '',  # blank label
    }

    size = ApparelSize(**data)

    assert size.labelSize == '-'
    assert size.customSize == 'CUSTOM'
    #
    @dataclass
    class Obj:
        apparelStyle: str
        labelSize: str | None
        customSize: str | None


    obj = Obj(apparelStyle='Unisex', labelSize=None, customSize=None)
    size = ApparelSize.model_validate(obj)
    assert size.apparelStyle == 'Unisex'
    assert size.labelSize == '-'
    assert size.customSize == 'CUSTOM'
