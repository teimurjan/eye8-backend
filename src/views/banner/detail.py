from src.validation_rules.banner.update import (
    UpdateBannerData,
    UpdateBannerDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.serializers.banner import BannerSerializer
from src.services.banner import BannerService
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class BannerDetailView(ValidatableView[UpdateBannerData]):
    def __init__(
        self,
        validator: UpdateBannerDataValidator,
        service: BannerService,
        serializer_cls: Type[BannerSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, banner_id: int):
        try:
            banner = self._service.get_one(banner_id)
            raw_intl = request.args.get("raw_intl") == "1"
            serialized_banner = (
                self._serializer_cls(banner)
                .in_language(None if raw_intl else request.language)
                .serialize()
            )
            return {"data": serialized_banner}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, banner_id: int):
        try:
            data = {
                **parse_json_from_form_data(request.form),
                "image": request.files.get("image") or request.form.get("image"),
            }
            valid_data = self._validate(data)
            banner = self._service.update(banner_id, valid_data, user=request.user)
            serialized_banner = self._serializer_cls(banner).serialize()
            return {"data": serialized_banner}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def delete(self, request: Request, banner_id: int):
        try:
            self._service.delete(banner_id, user=request.user)
            return {}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, banner_id: int):
        try:
            self._service.get_one(banner_id)
            return {}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE
