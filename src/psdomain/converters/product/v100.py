"""
Product Data v1.0.0 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.product import v100 as prod_conv

    # Pydantic -> Proto
    proto_response = prod_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = prod_conv.from_proto(proto_response)
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import TYPE_CHECKING

from psdomain.model.product_data.v_1_0_0 import (
    ProductResponseV100,
    ProductCloseOutResponseV100,
    ProductDateModifiedResponseV100,
    GetProductSellableResponseV100,
    ProductV100,
)
from psdomain.model.product_data.common import (
    Product,
    ProductPart,
    ProductPartArray,
    ProductCategory,
    ProductCategoryArray,
    RelatedProduct,
    RelatedProductArray,
    ProductKeyword,
    ProductKeywordArray,
    ProductMarketingPoint,
    ProductMarketingPointArray,
    ProductPrice,
    Color,
    ColorArray,
    PrimaryColor,
    Dimension,
    Specification,
    SpecificationArray,
    ApparelSize,
    ProductPackage,
    ProductPackagingArray,
    ShippingPackage,
    ShippingPackageArray,
    ProductCloseOut,
    ProductCloseOutArray,
    ProductDateModified,
    ProductDateModifiedArray,
    ProductSellable,
    ProductSellableArray,
)
from psdomain.model.base import ErrorMessage
from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty

if TYPE_CHECKING:
    from psdomain.proto.product import v100_pb2 as proto


# --- Helper converters for nested types ---

def color_to_proto(c: Color, proto_module) -> 'proto.ColorV100':
    result = proto_module.ColorV100(
        color_name=pydantic_str_or_empty(c.colorName),
    )
    if c.standardColorName:
        result.standard_color_name = c.standardColorName
    if c.hex:
        result.hex = c.hex
    if c.approximatePms:
        result.approximate_pms = c.approximatePms
    return result


def color_from_proto(p) -> Color:
    return Color(
        colorName=proto_str_or_none(p.color_name),
        standardColorName=proto_str_or_none(p.standard_color_name) if p.HasField('standard_color_name') else None,
        hex=proto_str_or_none(p.hex) if p.HasField('hex') else None,
        approximatePms=proto_str_or_none(p.approximate_pms) if p.HasField('approximate_pms') else None,
    )


def dimension_to_proto(d: Dimension, proto_module) -> 'proto.DimensionV100':
    result = proto_module.DimensionV100(
        dimension_uom=str(d.dimensionUom) if d.dimensionUom else "",
        weight_uom=str(d.weightUom) if d.weightUom else "",
    )
    if d.depth is not None:
        result.depth = str(d.depth)
    if d.height is not None:
        result.height = str(d.height)
    if d.width is not None:
        result.width = str(d.width)
    if d.weight is not None:
        result.weight = str(d.weight)
    return result


def dimension_from_proto(p) -> Dimension:
    from psdomain.model.base import DimensionUoM, WeightUoM
    dim_uom = None
    if p.dimension_uom:
        try:
            dim_uom = DimensionUoM(p.dimension_uom)
        except ValueError:
            pass
    weight_uom = None
    if p.weight_uom:
        try:
            weight_uom = WeightUoM(p.weight_uom)
        except ValueError:
            pass
    return Dimension(
        dimensionUom=dim_uom,
        depth=Decimal(p.depth) if p.HasField('depth') and p.depth else None,
        height=Decimal(p.height) if p.HasField('height') and p.height else None,
        width=Decimal(p.width) if p.HasField('width') and p.width else None,
        weightUom=weight_uom,
        weight=Decimal(p.weight) if p.HasField('weight') and p.weight else None,
    )


def specification_to_proto(s: Specification, proto_module) -> 'proto.SpecificationV100':
    result = proto_module.SpecificationV100(
        specification_type=str(s.specificationType) if s.specificationType else "",
        measurement_value=pydantic_str_or_empty(s.measurementValue),
    )
    if s.SpecificationUom:
        result.specification_uom = s.SpecificationUom
    return result


def specification_from_proto(p) -> Specification:
    from psdomain.model.product_data.common import SpecificationType
    spec_type = None
    if p.specification_type:
        try:
            spec_type = SpecificationType(p.specification_type)
        except ValueError:
            spec_type = p.specification_type
    return Specification(
        specificationType=spec_type,
        SpecificationUom=proto_str_or_none(p.specification_uom) if p.HasField('specification_uom') else None,
        measurementValue=proto_str_or_none(p.measurement_value),
    )


def apparel_size_to_proto(a: ApparelSize, proto_module) -> 'proto.ApparelSizeV100':
    result = proto_module.ApparelSizeV100(
        apparel_style=str(a.apparelStyle) if a.apparelStyle else "",
        label_size=pydantic_str_or_empty(a.labelSize),
    )
    if a.customSize:
        result.custom_size = a.customSize
    return result


def apparel_size_from_proto(p) -> ApparelSize:
    from psdomain.model.product_data.common import ApparelStyle
    style = None
    if p.apparel_style:
        try:
            style = ApparelStyle(p.apparel_style)
        except ValueError:
            style = p.apparel_style
    return ApparelSize(
        apparelStyle=style,
        labelSize=p.label_size,
        customSize=proto_str_or_none(p.custom_size) if p.HasField('custom_size') else None,
    )


def product_package_to_proto(pp: ProductPackage, proto_module) -> 'proto.ProductPackageV100':
    result = proto_module.ProductPackageV100(
        default=pp.default,
        package_type=pydantic_str_or_empty(pp.packageType),
        quantity=str(pp.quantity) if pp.quantity else "0",
        dimension_uom=str(pp.dimensionUom) if pp.dimensionUom else "",
        weight_uom=str(pp.weightUom) if pp.weightUom else "",
    )
    if pp.description:
        result.description = pp.description
    if pp.depth is not None:
        result.depth = str(pp.depth)
    if pp.height is not None:
        result.height = str(pp.height)
    if pp.width is not None:
        result.width = str(pp.width)
    if pp.weight is not None:
        result.weight = str(pp.weight)
    return result


def product_package_from_proto(p) -> ProductPackage:
    from psdomain.model.base import DimensionUoM, WeightUoM
    dim_uom = None
    if p.dimension_uom:
        try:
            dim_uom = DimensionUoM(p.dimension_uom)
        except ValueError:
            pass
    weight_uom = None
    if p.weight_uom:
        try:
            weight_uom = WeightUoM(p.weight_uom)
        except ValueError:
            pass
    return ProductPackage(
        default=p.default,
        packageType=proto_str_or_none(p.package_type),
        description=proto_str_or_none(p.description) if p.HasField('description') else None,
        quantity=Decimal(p.quantity) if p.quantity else Decimal(0),
        dimensionUom=dim_uom,
        depth=Decimal(p.depth) if p.HasField('depth') and p.depth else None,
        height=Decimal(p.height) if p.HasField('height') and p.height else None,
        width=Decimal(p.width) if p.HasField('width') and p.width else None,
        weightUom=weight_uom,
        weight=Decimal(p.weight) if p.HasField('weight') and p.weight else None,
    )


def shipping_package_to_proto(sp: ShippingPackage, proto_module) -> 'proto.ShippingPackageV100':
    result = proto_module.ShippingPackageV100(
        package_type=pydantic_str_or_empty(sp.packageType),
        quantity=str(sp.quantity) if sp.quantity else "0",
        dimension_uom=str(sp.dimensionUom) if sp.dimensionUom else "",
        weight_uom=str(sp.weightUom) if sp.weightUom else "",
    )
    if sp.description:
        result.description = sp.description
    if sp.depth is not None:
        result.depth = str(sp.depth)
    if sp.height is not None:
        result.height = str(sp.height)
    if sp.width is not None:
        result.width = str(sp.width)
    if sp.weight is not None:
        result.weight = str(sp.weight)
    return result


def shipping_package_from_proto(p) -> ShippingPackage:
    from psdomain.model.base import DimensionUoM, WeightUoM
    dim_uom = None
    if p.dimension_uom:
        try:
            dim_uom = DimensionUoM(p.dimension_uom)
        except ValueError:
            pass
    weight_uom = None
    if p.weight_uom:
        try:
            weight_uom = WeightUoM(p.weight_uom)
        except ValueError:
            pass
    return ShippingPackage(
        packageType=p.package_type,
        description=proto_str_or_none(p.description) if p.HasField('description') else None,
        quantity=Decimal(p.quantity) if p.quantity else Decimal(0),
        dimensionUom=dim_uom,
        depth=Decimal(p.depth) if p.HasField('depth') and p.depth else None,
        height=Decimal(p.height) if p.HasField('height') and p.height else None,
        width=Decimal(p.width) if p.HasField('width') and p.width else None,
        weightUom=weight_uom,
        weight=Decimal(p.weight) if p.HasField('weight') and p.weight else None,
    )


def product_price_to_proto(pp: ProductPrice, proto_module) -> 'proto.ProductPriceV100':
    result = proto_module.ProductPriceV100(
        quantity_min=pp.quantityMin,
        price=str(pp.price) if pp.price else "0",
    )
    if pp.quantityMax is not None:
        result.quantity_max = pp.quantityMax
    if pp.discountCode:
        result.discount_code = pp.discountCode
    return result


def product_price_from_proto(p) -> ProductPrice:
    return ProductPrice(
        quantityMin=p.quantity_min,
        quantityMax=p.quantity_max if p.HasField('quantity_max') else None,
        price=Decimal(p.price) if p.price else Decimal(0),
        discountCode=proto_str_or_none(p.discount_code) if p.HasField('discount_code') else None,
    )


def product_category_to_proto(pc: ProductCategory, proto_module) -> 'proto.ProductCategoryV100':
    result = proto_module.ProductCategoryV100(
        category=pydantic_str_or_empty(pc.category),
    )
    if pc.subCategory:
        result.sub_category = pc.subCategory
    return result


def product_category_from_proto(p) -> ProductCategory:
    return ProductCategory(
        category=proto_str_or_none(p.category),
        subCategory=proto_str_or_none(p.sub_category) if p.HasField('sub_category') else None,
    )


def related_product_to_proto(rp: RelatedProduct, proto_module) -> 'proto.RelatedProductV100':
    result = proto_module.RelatedProductV100(
        relation_type=str(rp.relationType) if rp.relationType else "",
        product_id=rp.productId,
    )
    if rp.partId:
        result.part_id = rp.partId
    return result


def related_product_from_proto(p) -> RelatedProduct:
    from psdomain.model.product_data.common import RelationTye
    rel_type = None
    if p.relation_type:
        try:
            rel_type = RelationTye(p.relation_type)
        except ValueError:
            rel_type = p.relation_type
    return RelatedProduct(
        relationType=rel_type,
        productId=p.product_id,
        partId=proto_str_or_none(p.part_id) if p.HasField('part_id') else None,
    )


def product_keyword_to_proto(pk: ProductKeyword, proto_module) -> 'proto.ProductKeywordV100':
    return proto_module.ProductKeywordV100(keyword=pk.keyword)


def product_keyword_from_proto(p) -> ProductKeyword:
    return ProductKeyword(keyword=p.keyword)


def marketing_point_to_proto(mp: ProductMarketingPoint, proto_module) -> 'proto.ProductMarketingPointV100':
    result = proto_module.ProductMarketingPointV100(
        point_copy=pydantic_str_or_empty(mp.pointCopy),
    )
    if mp.pointType:
        result.point_type = mp.pointType
    return result


def marketing_point_from_proto(p) -> ProductMarketingPoint:
    return ProductMarketingPoint(
        pointType=proto_str_or_none(p.point_type) if p.HasField('point_type') else None,
        pointCopy=proto_str_or_none(p.point_copy),
    )


# --- ProductPart converters ---

def product_part_to_proto(pp: ProductPart, proto_module) -> 'proto.ProductPartV100':
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.ProductPartV100(
        part_id=pp.partId,
        descriptions=pp.description or [],
    )

    if pp.primaryColor and pp.primaryColor.Color:
        result.primary_color.CopyFrom(color_to_proto(pp.primaryColor.Color, proto_module))

    if pp.countryOfOrigin:
        result.country_of_origin = pp.countryOfOrigin

    if pp.ColorArray:
        for c in pp.ColorArray.Color:
            result.colors.append(color_to_proto(c, proto_module))

    if pp.primaryMaterial:
        result.primary_material = pp.primaryMaterial

    if pp.SpecificationArray:
        for s in pp.SpecificationArray.Specification:
            result.specifications.append(specification_to_proto(s, proto_module))

    if pp.shape:
        result.shape = pp.shape

    if pp.ApparelSize:
        result.apparel_size.CopyFrom(apparel_size_to_proto(pp.ApparelSize, proto_module))

    if pp.Dimension:
        result.dimension.CopyFrom(dimension_to_proto(pp.Dimension, proto_module))

    if pp.leadTime is not None:
        result.lead_time = pp.leadTime

    if pp.unspsc:
        result.unspsc = pp.unspsc

    if pp.gtin:
        result.gtin = pp.gtin

    if pp.isRushService is not None:
        result.is_rush_service = pp.isRushService

    if pp.ProductPackagingArray:
        for pkg in pp.ProductPackagingArray.ProductPackage:
            result.product_packaging.append(product_package_to_proto(pkg, proto_module))

    if pp.ShippingPackageArray:
        for pkg in pp.ShippingPackageArray.ShippingPackage:
            result.shipping_packaging.append(shipping_package_to_proto(pkg, proto_module))

    if pp.endDate:
        ts = Timestamp()
        ts.FromDatetime(pp.endDate)
        result.end_date.CopyFrom(ts)

    if pp.effectiveDate:
        ts = Timestamp()
        ts.FromDatetime(pp.effectiveDate)
        result.effective_date.CopyFrom(ts)

    if pp.isCloseout is not None:
        result.is_closeout = pp.isCloseout

    if pp.isCaution is not None:
        result.is_caution = pp.isCaution

    if pp.cautionComment:
        result.caution_comment = pp.cautionComment

    if pp.nmfcCode is not None:
        result.nmfc_code = str(pp.nmfcCode)

    if pp.nmfcDescription:
        result.nmfc_description = pp.nmfcDescription

    if pp.nmfcNumber:
        result.nmfc_number = pp.nmfcNumber

    if pp.isOnDemand is not None:
        result.is_on_demand = pp.isOnDemand

    if pp.isHazmat is not None:
        result.is_hazmat = pp.isHazmat

    return result


def product_part_from_proto(p) -> ProductPart:
    primary_color = None
    if p.HasField('primary_color'):
        primary_color = PrimaryColor(Color=color_from_proto(p.primary_color))

    color_array = None
    if p.colors:
        color_array = ColorArray(Color=[color_from_proto(c) for c in p.colors])

    spec_array = None
    if p.specifications:
        spec_array = SpecificationArray(Specification=[specification_from_proto(s) for s in p.specifications])

    apparel_size = None
    if p.HasField('apparel_size'):
        apparel_size = apparel_size_from_proto(p.apparel_size)

    dimension = None
    if p.HasField('dimension'):
        dimension = dimension_from_proto(p.dimension)

    product_packaging = None
    if p.product_packaging:
        product_packaging = ProductPackagingArray(
            ProductPackage=[product_package_from_proto(pkg) for pkg in p.product_packaging]
        )

    shipping_packaging = None
    if p.shipping_packaging:
        shipping_packaging = ShippingPackageArray(
            ShippingPackage=[shipping_package_from_proto(pkg) for pkg in p.shipping_packaging]
        )

    end_date = None
    if p.HasField('end_date'):
        end_date = p.end_date.ToDatetime()

    effective_date = None
    if p.HasField('effective_date'):
        effective_date = p.effective_date.ToDatetime()

    return ProductPart(
        partId=p.part_id,
        description=list(p.descriptions),
        primaryColor=primary_color,
        countryOfOrigin=proto_str_or_none(p.country_of_origin) if p.HasField('country_of_origin') else None,
        ColorArray=color_array,
        primaryMaterial=proto_str_or_none(p.primary_material) if p.HasField('primary_material') else None,
        SpecificationArray=spec_array,
        shape=proto_str_or_none(p.shape) if p.HasField('shape') else None,
        ApparelSize=apparel_size,
        Dimension=dimension,
        leadTime=p.lead_time if p.HasField('lead_time') else None,
        unspsc=proto_str_or_none(p.unspsc) if p.HasField('unspsc') else None,
        gtin=proto_str_or_none(p.gtin) if p.HasField('gtin') else None,
        isRushService=p.is_rush_service if p.HasField('is_rush_service') else None,
        ProductPackagingArray=product_packaging,
        ShippingPackageArray=shipping_packaging,
        endDate=end_date,
        effectiveDate=effective_date,
        isCloseout=p.is_closeout if p.HasField('is_closeout') else None,
        isCaution=p.is_caution if p.HasField('is_caution') else None,
        cautionComment=proto_str_or_none(p.caution_comment) if p.HasField('caution_comment') else None,
        nmfcCode=Decimal(p.nmfc_code) if p.HasField('nmfc_code') and p.nmfc_code else None,
        nmfcDescription=proto_str_or_none(p.nmfc_description) if p.HasField('nmfc_description') else None,
        nmfcNumber=proto_str_or_none(p.nmfc_number) if p.HasField('nmfc_number') else None,
        isOnDemand=p.is_on_demand if p.HasField('is_on_demand') else None,
        isHazmat=p.is_hazmat if p.HasField('is_hazmat') else None,
    )


# --- Product converters ---

def product_to_proto(prod: Product, proto_module) -> 'proto.ProductV100':
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.ProductV100(
        product_id=prod.productId,
        product_name=prod.productName,
        descriptions=prod.description or [],
    )

    if prod.priceExpiresDate:
        ts = Timestamp()
        ts.FromDatetime(prod.priceExpiresDate)
        result.price_expires_date.CopyFrom(ts)

    if prod.ProductMarketingPointArray:
        for mp in prod.ProductMarketingPointArray.ProductMarketingPoint:
            result.marketing_points.append(marketing_point_to_proto(mp, proto_module))

    if prod.ProductKeywordArray:
        for kw in prod.ProductKeywordArray.ProductKeyword:
            result.keywords.append(product_keyword_to_proto(kw, proto_module))

    if prod.productBrand:
        result.product_brand = prod.productBrand

    if prod.export is not None:
        result.export = prod.export

    if prod.ProductCategoryArray:
        for cat in prod.ProductCategoryArray.ProductCategory:
            result.categories.append(product_category_to_proto(cat, proto_module))

    if prod.RelatedProductArray:
        for rp in prod.RelatedProductArray.RelatedProduct:
            result.related_products.append(related_product_to_proto(rp, proto_module))

    if prod.primaryImageURL:
        result.primary_image_url = prod.primaryImageURL

    # V1.0.0 has prices directly on product (ProductPriceArray), not price groups
    # Using first price group if available
    if prod.ProductPriceGroupArray:
        for pg in prod.ProductPriceGroupArray.ProductPriceGroup:
            if pg.ProductPriceArray:
                for price in pg.ProductPriceArray.ProductPrice:
                    result.prices.append(product_price_to_proto(price, proto_module))
                break

    if prod.complianceInfoAvailable is not None:
        result.compliance_info_available = prod.complianceInfoAvailable

    if prod.ProductPartArray:
        for part in prod.ProductPartArray.ProductPart:
            result.parts.append(product_part_to_proto(part, proto_module))

    if prod.lastChangeDate:
        ts = Timestamp()
        ts.FromDatetime(prod.lastChangeDate)
        result.last_change_date.CopyFrom(ts)

    if prod.creationDate:
        ts = Timestamp()
        ts.FromDatetime(prod.creationDate)
        result.creation_date.CopyFrom(ts)

    if prod.endDate:
        ts = Timestamp()
        ts.FromDatetime(prod.endDate)
        result.end_date.CopyFrom(ts)

    if prod.effectiveDate:
        ts = Timestamp()
        ts.FromDatetime(prod.effectiveDate)
        result.effective_date.CopyFrom(ts)

    if prod.isCaution is not None:
        result.is_caution = prod.isCaution

    if prod.cautionComment:
        result.caution_comment = prod.cautionComment

    if prod.isCloseout is not None:
        result.is_closeout = prod.isCloseout

    if prod.lineName:
        result.line_name = prod.lineName

    return result


def product_from_proto(p) -> ProductV100:
    price_expires = None
    if p.HasField('price_expires_date'):
        price_expires = p.price_expires_date.ToDatetime()

    marketing_points = None
    if p.marketing_points:
        marketing_points = ProductMarketingPointArray(
            ProductMarketingPoint=[marketing_point_from_proto(mp) for mp in p.marketing_points]
        )

    keywords = None
    if p.keywords:
        keywords = ProductKeywordArray(
            ProductKeyword=[product_keyword_from_proto(kw) for kw in p.keywords]
        )

    categories = None
    if p.categories:
        categories = ProductCategoryArray(
            ProductCategory=[product_category_from_proto(cat) for cat in p.categories]
        )

    related_products = None
    if p.related_products:
        related_products = RelatedProductArray(
            RelatedProduct=[related_product_from_proto(rp) for rp in p.related_products]
        )

    parts = ProductPartArray(ProductPart=[])
    if p.parts:
        parts = ProductPartArray(
            ProductPart=[product_part_from_proto(part) for part in p.parts]
        )

    last_change_date = None
    if p.HasField('last_change_date'):
        last_change_date = p.last_change_date.ToDatetime()

    creation_date = None
    if p.HasField('creation_date'):
        creation_date = p.creation_date.ToDatetime()

    end_date = None
    if p.HasField('end_date'):
        end_date = p.end_date.ToDatetime()

    effective_date = None
    if p.HasField('effective_date'):
        effective_date = p.effective_date.ToDatetime()

    return ProductV100(
        productId=p.product_id,
        productName=p.product_name,
        description=list(p.descriptions) if p.descriptions else None,
        priceExpiresDate=price_expires,
        ProductMarketingPointArray=marketing_points,
        ProductKeywordArray=keywords,
        productBrand=proto_str_or_none(p.product_brand) if p.HasField('product_brand') else None,
        export=p.export if p.HasField('export') else None,
        ProductCategoryArray=categories,
        RelatedProductArray=related_products,
        primaryImageURL=proto_str_or_none(p.primary_image_url) if p.HasField('primary_image_url') else None,
        complianceInfoAvailable=p.compliance_info_available if p.HasField('compliance_info_available') else None,
        ProductPartArray=parts,
        lastChangeDate=last_change_date,
        creationDate=creation_date,
        endDate=end_date,
        effectiveDate=effective_date,
        isCaution=p.is_caution if p.HasField('is_caution') else None,
        cautionComment=proto_str_or_none(p.caution_comment) if p.HasField('caution_comment') else None,
        isCloseout=p.is_closeout if p.HasField('is_closeout') else None,
        lineName=proto_str_or_none(p.line_name) if p.HasField('line_name') else None,
    )


# --- ErrorMessage converters ---

def error_message_to_proto(msg: ErrorMessage, proto_module):
    return proto_module.ErrorMessage(
        code=msg.code,
        description=msg.description,
    )


def error_message_from_proto(p) -> ErrorMessage:
    return ErrorMessage(
        code=p.code,
        description=p.description,
    )


# --- ProductGroup converters (for closeout, sellable, date_modified) ---

def product_group_to_proto(product_id: str, part_ids: list[str], proto_module) -> 'proto.ProductGroupV100':
    result = proto_module.ProductGroupV100(product_id=product_id)
    result.part_ids.extend(part_ids)
    return result


def product_closeout_array_to_proto(arr: ProductCloseOutArray, proto_module) -> list:
    """Convert ProductCloseOutArray to list of ProductGroupV100."""
    # Group by product_id
    grouped = defaultdict(list)
    for item in arr.ProductCloseOut:
        if item.partId:
            grouped[item.productId].append(item.partId)
        else:
            grouped[item.productId]  # ensure key exists even without partId

    return [
        product_group_to_proto(prod_id, part_ids, proto_module)
        for prod_id, part_ids in grouped.items()
    ]


def product_closeout_array_from_proto(products) -> ProductCloseOutArray:
    """Convert list of ProductGroupV100 to ProductCloseOutArray."""
    items = []
    for pg in products:
        if pg.part_ids:
            for part_id in pg.part_ids:
                items.append(ProductCloseOut(productId=pg.product_id, partId=part_id))
        else:
            items.append(ProductCloseOut(productId=pg.product_id, partId=None))
    return ProductCloseOutArray(ProductCloseOut=items)


def product_sellable_array_to_proto(arr: ProductSellableArray, proto_module) -> list:
    """Convert ProductSellableArray to list of ProductGroupV100."""
    grouped = defaultdict(list)
    for item in arr.ProductSellable:
        if item.partId:
            grouped[item.productId].append(item.partId)
        else:
            grouped[item.productId]

    return [
        product_group_to_proto(prod_id, part_ids, proto_module)
        for prod_id, part_ids in grouped.items()
    ]


def product_sellable_array_from_proto(products) -> ProductSellableArray:
    """Convert list of ProductGroupV100 to ProductSellableArray."""
    items = []
    for pg in products:
        if pg.part_ids:
            for part_id in pg.part_ids:
                items.append(ProductSellable(productId=pg.product_id, partId=part_id))
        else:
            items.append(ProductSellable(productId=pg.product_id, partId=None))
    return ProductSellableArray(ProductSellable=items)


def product_date_modified_array_to_proto(arr: ProductDateModifiedArray, proto_module) -> list:
    """Convert ProductDateModifiedArray to list of ProductGroupV100."""
    grouped = defaultdict(list)
    for item in arr.ProductDateModified:
        if item.partId:
            grouped[item.productId].append(item.partId)
        else:
            grouped[item.productId]

    return [
        product_group_to_proto(prod_id, part_ids, proto_module)
        for prod_id, part_ids in grouped.items()
    ]


def product_date_modified_array_from_proto(products) -> ProductDateModifiedArray:
    """Convert list of ProductGroupV100 to ProductDateModifiedArray."""
    items = []
    for pg in products:
        if pg.part_ids:
            for part_id in pg.part_ids:
                items.append(ProductDateModified(productId=pg.product_id, partId=part_id))
        else:
            items.append(ProductDateModified(productId=pg.product_id, partId=None))
    return ProductDateModifiedArray(ProductDateModified=items)


# --- Response converters (Public API) ---

def product_response_to_proto(response: ProductResponseV100):
    """Convert pydantic ProductResponseV100 to proto GetProductResponseV100."""
    from psdomain.proto.product import v100_pb2 as proto_module

    result = proto_module.GetProductResponseV100()
    if response.Product:
        result.product.CopyFrom(product_to_proto(response.Product, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def product_response_from_proto(proto_msg) -> ProductResponseV100:
    """Convert proto GetProductResponseV100 to pydantic ProductResponseV100."""
    product = None
    if proto_msg.HasField('product'):
        product = product_from_proto(proto_msg.product)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return ProductResponseV100(
        Product=product,
        ErrorMessage=error_msg,
    )


def closeout_response_to_proto(response: ProductCloseOutResponseV100):
    """Convert pydantic ProductCloseOutResponseV100 to proto GetProductCloseOutResponseV100."""
    from psdomain.proto.product import v100_pb2 as proto_module

    result = proto_module.GetProductCloseOutResponseV100()
    if response.ProductCloseOutArray:
        for pg in product_closeout_array_to_proto(response.ProductCloseOutArray, proto_module):
            result.products.append(pg)
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def closeout_response_from_proto(proto_msg) -> ProductCloseOutResponseV100:
    """Convert proto GetProductCloseOutResponseV100 to pydantic ProductCloseOutResponseV100."""
    closeout_array = None
    if proto_msg.products:
        closeout_array = product_closeout_array_from_proto(proto_msg.products)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return ProductCloseOutResponseV100(
        ProductCloseOutArray=closeout_array,
        ErrorMessage=error_msg,
    )


def sellable_response_to_proto(response: GetProductSellableResponseV100):
    """Convert pydantic GetProductSellableResponseV100 to proto GetProductSellableResponseV100."""
    from psdomain.proto.product import v100_pb2 as proto_module

    result = proto_module.GetProductSellableResponseV100()
    if response.ProductSellableArray:
        for pg in product_sellable_array_to_proto(response.ProductSellableArray, proto_module):
            result.products.append(pg)
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def sellable_response_from_proto(proto_msg) -> GetProductSellableResponseV100:
    """Convert proto GetProductSellableResponseV100 to pydantic GetProductSellableResponseV100."""
    sellable_array = None
    if proto_msg.products:
        sellable_array = product_sellable_array_from_proto(proto_msg.products)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return GetProductSellableResponseV100(
        ProductSellableArray=sellable_array,
        ErrorMessage=error_msg,
    )


def date_modified_response_to_proto(response: ProductDateModifiedResponseV100):
    """Convert pydantic ProductDateModifiedResponseV100 to proto GetProductDateModifiedResponseV100."""
    from psdomain.proto.product import v100_pb2 as proto_module

    result = proto_module.GetProductDateModifiedResponseV100()
    if response.ProductDateModifiedArray:
        for pg in product_date_modified_array_to_proto(response.ProductDateModifiedArray, proto_module):
            result.products.append(pg)
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def date_modified_response_from_proto(proto_msg) -> ProductDateModifiedResponseV100:
    """Convert proto GetProductDateModifiedResponseV100 to pydantic ProductDateModifiedResponseV100."""
    date_modified_array = None
    if proto_msg.products:
        date_modified_array = product_date_modified_array_from_proto(proto_msg.products)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return ProductDateModifiedResponseV100(
        ProductDateModifiedArray=date_modified_array,
        ErrorMessage=error_msg,
    )


# Convenience aliases for main endpoint
to_proto = product_response_to_proto
from_proto = product_response_from_proto
