from src.validation_rules.banner.create import (
    CreateBannerData,
    CreateBannerDataValidator,
)
from src.utils.request import Request
from src.serializers.banner import BannerSerializer
from typing import Type
from src.services.banner import BannerService
from src.constants.status_codes import OK_CODE
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class BannerListView(ValidatableView[CreateBannerData]):
    def __init__(
        self,
        validator: CreateBannerDataValidator,
        service: BannerService,
        serializer_cls: Type[BannerSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        banners = self._service.get_all()
        raw_intl = request.args.get("raw_intl") == "1"
        serialized_banners = [
            self._serializer_cls(category)
            .in_language(None if raw_intl else request.language)
            .serialize()
            for category in banners
        ]
        return {"data": serialized_banners}, OK_CODE

    def post(self, request: Request):
        parsed_json_data = parse_json_from_form_data(request.form)
        image = request.files.get("image")
        valid_data = self._validate({**parsed_json_data, "image": image})
        banner = self._service.create(valid_data, user=request.user)
        serialized_banners = self._serializer_cls(banner).serialize()
        return {"data": serialized_banners}, OK_CODE
