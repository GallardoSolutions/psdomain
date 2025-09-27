import os
from datetime import datetime

# reference https://tools.promostandards.org/media-content-1-1-0
from . import base

THUMBNAIL_SIZE = 50
SMALL_SIZE = 470
BASE_SIZE = 1100
BEST_SIZE = 1900

PS_MEDX_HOST = os.getenv('PS_MEDX_HOST', 'https://psmedx.com/')


class MediaType(base.StrEnum):
    """
    Media Types allowed in the MediaContent service.
    """
    IMAGE = 'Image'
    VIDEO = 'Video'
    AUDIO = 'Audio'
    DOCUMENT = 'Document'


class ClassType(base.PSBaseModel):
    classTypeId: int
    classTypeName: str

    @classmethod
    def from_class_type_id(cls, class_type_id: int):
        names = {
            BLANK: 'Blank',
            DECORATED: 'Decorated',
            FRONT: 'Front',
            REAR: 'Rear',
            ALTERNATE: 'Alternate',
            SWATCH: 'Swatch',
            PRIMARY: 'Primary',
            RIGHT: 'Right',
            LEFT: 'Left',
            TOP: 'Top',
            BOTTOM: 'Bottom',
            INSIDE: 'Inside',
            OUTSIDE: 'Outside',
            STANDARD: 'Standard Definition',
            HIGH: 'High Definition',
            PODCAST: 'Podcast',
            SPECS: 'Specification Sheets',
            PRODUCT_SAFETY: 'Product Safety Information',
            FACTS: 'Fact Sheets',
            COMPLIANCE: 'Compliance Documents',
            ART_TEMPLATE: 'Art Templates',
            MARKETING: 'Marketing Material'
        }
        class_type_name = names.get(class_type_id, 'Custom')
        return cls(classTypeId=class_type_id, classTypeName=class_type_name)

    @property
    def is_blank(self):
        return self.classTypeId == BLANK

    @property
    def is_decorated(self):
        return self.classTypeId == DECORATED


class ClassTypeArray(base.PSBaseModel):
    ClassType: list[ClassType]

    @classmethod
    def from_class_types(cls, class_types: list[int]):
        return cls(ClassType=[ClassType.from_class_type_id(ct) for ct in class_types])

    def _get_class_types(self):
        return {ct.classTypeId for ct in self.ClassType}

    def get_class_types(self):
        class_type_set = getattr(self, '_class_type_set', None)
        if class_type_set is None:
            class_type_set = self._get_class_types()
            setattr(self, '_class_type_set', class_type_set)
        return class_type_set

    @property
    def names(self):
        return ', '.join(self.names_list)

    @property
    def names_list(self):
        return [obj.classTypeName for obj in self.ClassType]


class Decoration(base.PSBaseModel):
    decorationId: int
    decorationName: str

    @property
    def is_blank(self):
        return self.decorationName.lower() == 'blank'  # HIT has a decoration with name 'Blank'


class DecorationArray(base.PSBaseModel):
    Decoration: list[Decoration]

    @property
    def names(self):
        return ', '.join(self.names_list)

    @property
    def names_list(self):
        return [dec.decorationName for dec in self.Decoration]


class Location(base.PSBaseModel):
    locationId: int
    locationName: str


class LocationArray(base.PSBaseModel):
    Location: list[Location]

    @property
    def names(self):
        return ', '.join(self.names_list)

    @property
    def names_list(self):
        return [loc.locationName for loc in self.Location]


# Some ClassTypeOptions
INTERNAL = 900  # Internal Use
# Valid values for class type and class name:
# classType	Class Name	Description
# 0-499	    Reserved	Reserved for future use
# 500-999	Custom	    Custom class types for implementation specific use.
FRONT = 1007  # Front view
REAR = 1008  # Rear view
UNSPECIFIED = 1000  # Unspecified, Unknown or unspecified shot. This value means the shot type is unavailable for
# the media type.  # noqa
BLANK = 1001  # The shot is of blank media
DECORATED = 1002  # The shot is of decorated media
ALTERNATE = 1003  # The shot is alternate. This may indicate the product is combined with other media to stage a scene.
SWATCH = 1004  # The shot is of a swatch
CUSTOM = 1005  # The shot is custom which does not fall into any specific type
PRIMARY = 1006  # The primary image
RIGHT = 1009  # Right view
LEFT = 1010  # Left view
TOP = 1011  # Top view
BOTTOM = 1012  # Bottom view
INSIDE = 1013  # Inside view
OUTSIDE = 1014  # Outside view
# The next ones are mostly for videos
STANDARD = 2000  # Standard Definition
HIGH = 2001  # High definition
#
PODCAST = 3000  # Podcast
#
SPECS = 4000  # Specification sheets
PRODUCT_SAFETY = 4001  # Product safety information
FACTS = 4002  # Fact sheets
COMPLIANCE = 4003  # Compliance documents
ART_TEMPLATE = 4004  # Art templates
MARKETING = 4005  # Marketing material


class MediaContent(base.PSBaseModel):
    productId: str
    partId: str | None = None
    url: str | None = None
    mediaType: str
    fileSize: float | None = None
    width: int | None = None
    height: int | None = None
    dpi: int | None = None
    color: str | None = None
    description: str | None = None
    singlePart: bool
    changeTimeStamp: datetime | None = None
    ClassTypeArray: ClassTypeArray
    DecorationArray: DecorationArray | None
    LocationArray: LocationArray | None

    # decorationId: int | None  # Appears in the WSDL but Deprecated. Use DecorationArray.

    def __lt__(self, other):
        class_types = self.get_class_types()
        if self.width and self.is_small and {FRONT, BLANK}.intersection(class_types) == {FRONT, BLANK}:
            return True
        if self.width and self.is_small and self.is_front:
            return True
        if self.width and self.is_small:
            return True
        return False

    @property
    def is_small(self):
        return self.height == SMALL_SIZE

    @property
    def image_size(self):
        return f'{self.width}x{self.height}'

    def get_class_types(self):
        return self.ClassTypeArray.get_class_types()

    def all_class_types_are_equal(self, other):
        if len(self.ClassTypeArray.ClassType) == len(other.ClassTypeArray.ClassType):
            my_cls_types = self.get_class_types()
            other_cls_types = other.get_class_types()
            return my_cls_types == other_cls_types
        return False

    def __eq__(self, other: 'MediaContent'):
        return (self.same_resolution(other) and self.all_class_types_are_equal(other) and
                self.singlePart == other.singlePart and self.same_media_type(other) and self.same_color(other))

    def same_color(self, other: 'MediaContent'):
        return self.color == other.color

    def same_media_type(self, other: 'MediaContent'):
        return self.mediaType == other.mediaType

    def same_resolution(self, other: 'MediaContent'):
        return self.width == other.width and self.height == other.height

    @property
    def is_image(self):
        return self.mediaType == MediaType.IMAGE

    @property
    def is_blank(self):
        ret = BLANK in self.get_class_types()
        if ret:
            return not self.is_decorated  # Sometimes HIT has BLANK and Laser Engraving
        # hit has a Blank decoration
        return self.only_blank_decoration()

    @property
    def is_decorated(self):
        if DECORATED in self.get_class_types():
            return True
        non_blank_decoration = (dec for dec in self.decorations if not dec.is_blank)
        return any(non_blank_decoration)

    @property
    def is_primary(self):
        return PRIMARY in self.get_class_types()

    @property
    def is_high_res(self):
        return (self.height and self.height >= 1000) or \
            (self.dpi and self.dpi > 300) or \
            HIGH in self.get_class_types()

    @property
    def is_art_template(self):
        return ART_TEMPLATE in self.get_class_types()

    @property
    def decorations(self):
        return self.DecorationArray.Decoration if self.DecorationArray else []

    def only_blank_decoration(self):
        """
        HIT has a Blank decoration
        """
        return len(self.decorations) == 1 and self.decorations[0].is_blank

    def lt_single_part_blank_size(self, other: 'MediaContent', size: int):
        # Compare singlePart
        if self.singlePart != other.singlePart:
            return True if self.singlePart else False
        # Compare is_blank
        if self.is_blank != other.is_blank:
            return True if self.is_blank else False
        # compare front
        if self.is_front != other.is_front:
            return True if self.is_front else False

        # Compare height difference from size
        mc1_height_diff = abs(self.height - size) if self.height is not None else float('inf')
        mc2_height_diff = abs(other.height - size) if other.height is not None else float('inf')

        return mc1_height_diff < mc2_height_diff

    def lt_single_part_primary_size(self, other: 'MediaContent', size: int):
        # Compare single part & primary & front
        if self.singlePart != other.singlePart:
            return True if self.singlePart else False
        # Compare is_primary
        if self.is_primary != other.is_primary:
            return True if self.is_primary else False
        # compare front
        if self.is_front != other.is_front:
            return True if self.is_front else False

        # Compare height difference from size
        mc1_height_diff = abs(self.height - size) if self.height is not None else float('inf')
        mc2_height_diff = abs(other.height - size) if other.height is not None else float('inf')

        return mc1_height_diff < mc2_height_diff

    def lt_dimension(self, other: 'MediaContent'):
        mc1_height = self.height or float('inf')
        mc2_height = other.height or float('inf')
        return mc1_height < mc2_height

    @property
    def is_front(self):
        return FRONT in self.get_class_types()

    @property
    def is_rear(self):
        return REAR in self.get_class_types()

    @property
    def is_alternate(self):
        return ALTERNATE in self.get_class_types()

    @property
    def is_group(self):
        return not self.singlePart

    @property
    def is_swatch(self):
        return SWATCH in self.get_class_types()

    @property
    def is_displayable(self):
        return self.is_image and self.url and not self.url.lower().endswith(('.psd', '.pdf'))

    def lt_blank_thumbnail(self, other: 'MediaContent'):
        return self.lt_single_part_blank_size(other, THUMBNAIL_SIZE)

    def lt_blank_small(self, other: 'MediaContent'):
        return self.lt_single_part_blank_size(other, SMALL_SIZE)

    def lt_blank_base(self, other: 'MediaContent'):
        return self.lt_single_part_blank_size(other, BASE_SIZE)

    def lt_primary_base(self, other: 'MediaContent'):
        return self.lt_single_part_primary_size(other, BASE_SIZE)

    @property
    def standard_url(self):
        # if size > 25 MG, return resize from psmedx
        if self.is_too_big:
            return f'{PS_MEDX_HOST}resize/?image_url={self.url}&width={BEST_SIZE}'
        return self.url

    @property
    def is_too_big(self):
        # 25 MB
        max_size = 25 * 1000 * 1000
        return (self.fileSize and self.fileSize >= max_size) or (self.width and self.width > 2000) \
            or (self.height and self.height > 2000)


class MediaContentArray(base.PSBaseModel):
    MediaContent: list[MediaContent]


class MediaResponse(base.PSBaseModel):
    errorMessage: base.ErrorMessage | None

    @property
    def is_ok(self):
        return self.errorMessage is None

    @property
    def errors(self):
        return str(self.errorMessage) if self.errorMessage else None


class MediaContentDetailsResponse(MediaResponse):
    MediaContentArray: MediaContentArray | None

    def _get_media_content(self) -> list[MediaContent]:
        return self.MediaContentArray.MediaContent if self.MediaContentArray else []

    def _set_media_content(self, media_content: list[MediaContent]) -> None:
        self.MediaContentArray = MediaContentArray(MediaContent=media_content)

    MediaContent = property(_get_media_content, _set_media_content)

    def new_without_broken_links(self, broken_urls: list[str]) -> 'MediaContentDetailsResponse':
        media_content = [mc for mc in self.MediaContent if mc.url not in broken_urls]
        return self.__class__.from_media_content(media_content)

    @classmethod
    def from_media_content(cls, media_content: list[MediaContent]) -> 'MediaContentDetailsResponse':
        return cls(MediaContentArray=MediaContentArray(MediaContent=media_content), errorMessage=None)

    def get_unique_urls(self) -> set[str]:
        return {mc.url for mc in self.MediaContent}


# Media Content Modified Since

class MediaContentModifiedSinceRequest(base.PSBaseModel):
    wsVersion: str
    id: str
    password: str | None
    cultureName: str | None
    changeTimeStamp: datetime | None


class MediaDateModified(base.PSBaseModel):
    productId: str
    partId: str | None = None


class MediaDateModifiedArray(base.PSBaseModel):
    MediaDateModified: list[MediaDateModified]


class GetMediaDateModifiedResponse(MediaResponse):
    MediaDateModifiedArray: MediaDateModifiedArray | None
