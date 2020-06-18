from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.promo_code import PromoCodeService
from src.utils.number import parse_int
from src.views.base import ValidatableView


class PromoCodeListView(ValidatableView):
    def __init__(self, validator, service: PromoCodeService, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        promo_codes, _ = self._service.get_all(user=request.user)

        serialized_promo_codes = [
            self
            ._serializer_cls(promo_code)
            .in_language(request.language)
            .serialize()
            for promo_code in promo_codes
        ]
        return {'data': serialized_promo_codes}, OK_CODE

    def post(self, request):
        try:
            data = request.get_json()
            self._validate(data)
            promo_code = self._service.create(data, user=request.user)
            serialized_promo_code = (
                self.
                _serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {'data': serialized_promo_code}, OK_CODE
        except self._service.ValueNotUnique:
            raise InvalidEntityFormat({'value': 'errors.alreadyExists'})
