from psdomain.model.media_content import MediaContentDetailsResponse, MediaContent


class MediaContentService:
    def __init__(self, media_content_response: MediaContentDetailsResponse, remove_broken_images=True):
        self.media_content_response = media_content_response

    @property
    def images(self) -> list[MediaContent]:
        return [mc for mc in self.media_content_response.MediaContent if mc.is_image]

    @property
    def different_dimensions(self):
        return any((mc.height for mc in self.images))

    @property
    def highest_resolution(self):
        return max((mc.height for mc in self.images if mc.height), default=0)

    @property
    def best_images(self):
        if self.different_dimensions:
            return [mc for mc in self.images if mc.height == self.highest_resolution]
        return self.images

    def get_blank_thumbnail_for_product(self, product_id: str) -> str:
        return self._get_blank_image_for_product(product_id, MediaContent.lt_blank_thumbnail)

    def get_blank_small_for_product(self, product_id: str) -> str:
        return self._get_blank_image_for_product(product_id, MediaContent.lt_blank_small)

    def get_blank_base_for_product(self, product_id: str) -> str:
        return self._get_blank_image_for_product(product_id, MediaContent.lt_blank_base)

    def get_blank_thumbnail_for_part(self, part_id: str) -> str:
        return self._get_blank_image_for_part(part_id, MediaContent.lt_blank_thumbnail)

    def get_blank_small_for_part(self, part_id: str) -> str:
        return self._get_blank_image_for_part(part_id, MediaContent.lt_blank_small)

    def get_blank_base_for_part(self, part_id: str) -> str:
        return self._get_blank_image_for_part(part_id, MediaContent.lt_blank_base)

    def get_blank_base_for_color(self, color: str) -> str:
        return self._get_blank_image_for_part_color(color, MediaContent.lt_blank_base)

    def _get_blank_image_for_product(self, product_id: str, method) -> str:
        MediaContent.__lt__ = method  # MediaContent.lt_blank_thumbnail
        filtered_images = self.filter_by_product_id(product_id)
        new_medias = sorted(filtered_images) if filtered_images else sorted(self.images)
        return new_medias[0].url if new_medias else ''

    def _get_blank_image_for_part(self, part_id: str, method) -> str:
        MediaContent.__lt__ = method  # MediaContent.lt_blank_thumbnail
        filtered_images = self.filter_by_part_id(part_id)
        new_medias = sorted(filtered_images)
        return new_medias[0].url if new_medias else ''

    def _get_blank_image_for_part_color(self, color: str, method) -> str:
        MediaContent.__lt__ = method  # MediaContent.lt_blank_thumbnail
        filtered_images = self.filter_by_color(color)
        new_medias = sorted(filtered_images)
        return new_medias[0].url if new_medias else ''

    def filter_by_part_id(self, part_id: str, only_highest_resolution=False) -> list[MediaContent]:
        images = self.best_images if only_highest_resolution else self.images
        return [mc for mc in images if mc.partId == part_id]

    def filter_by_color(self, color: str, only_highest_resolution=False) -> list[MediaContent]:
        color = color.lower()
        images = self.best_images if only_highest_resolution else self.images
        return [mc for mc in images if mc.color and mc.color.lower() == color]

    def filter_by_product_id(self, product_id: str, only_highest_resolution=False) -> list[MediaContent]:
        images = self.best_images if only_highest_resolution else self.images
        return [mc
                for mc in images
                if mc.productId == product_id and (mc.partId is None or mc.partId == product_id)]

    def rest_of_images_for_product(self, product_id: str, url: str) -> list[MediaContent]:
        return [
            mc
            for mc in self.filter_by_product_id(product_id, only_highest_resolution=True)
            if mc.url != url
        ]

    def rest_of_images_for_part(self, part_id: str, url: str) -> list[MediaContent]:
        return [
            mc
            for mc in self.filter_by_part_id(part_id, only_highest_resolution=True)
            if mc.url != url
        ]

    def rest_of_images_for_color(self, color: str, url: str) -> list[MediaContent]:
        return [
            mc
            for mc in self.filter_by_color(color, only_highest_resolution=True)
            if mc.url != url
        ]
