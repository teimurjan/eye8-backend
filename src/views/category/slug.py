from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.category import CategorySerializer
from src.services.category import CategoryService
from src.views.base import ValidatableView


class CategorySlugView:
    def __init__(self, service: CategoryService, serializer_cls: CategorySerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, slug):
        try:
            category = self._service.get_one_by_slug(slug)
            serialized_category = self._serializer_cls(
                category).in_language(request.language).serialize()
            return {'data': serialized_category}, OK_CODE
        except self._service.CategoryNotFound:
            return {}, NOT_FOUND_CODE
