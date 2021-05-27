from src.models.banner import Banner
from src.serializers.intl import IntlSerializer


class BannerSerializer(IntlSerializer):
    def __init__(self, banner: Banner):
        super().__init__()
        self._id = banner.id
        self._text_en = banner.text_en
        self._text_ru = banner.text_ru
        self._link_text_en = banner.link_text_en
        self._link_text_ru = banner.link_text_ru
        self._link = banner.link
        self._image = banner.image
        self._text_color = banner.text_color
        self._text_top_offset = banner.text_top_offset
        self._text_left_offset = banner.text_left_offset
        self._text_right_offset = banner.text_right_offset
        self._text_bottom_offset = banner.text_bottom_offset
        self._created_on = banner.created_on
        self._updated_on = banner.updated_on

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "text": self._get_intl_field_from("text", self),
                "link_text": self._get_intl_field_from("link_text", self),
                "link": self._link,
                "text_color": self._text_color,
                "image": self._image,
                "text_top_offset": self._text_top_offset,
                "text_left_offset": self._text_left_offset,
                "text_right_offset": self._text_right_offset,
                "text_bottom_offset": self._text_bottom_offset,
                "created_on": self._created_on,
                "updated_on": self._updated_on,
            }
        )

