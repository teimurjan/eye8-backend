CREATE_PROMO_CODE_VALIDATION_RULES = {
    'discount': {'type': 'integer', 'required': True, 'min': -1, 'max': 100, 'nullable': False},
    'amount': {'type': 'integer', 'required': False, 'nullable': True},
    'value': {'type': 'string', 'required': True, 'nullable': False, 'maxlength': 60},
    'is_active': {'type': 'boolean', 'required': False, 'nullable': False},
    'disable_on_use': {'type': 'boolean', 'required': False, 'nullable': False},
    'products':  {
        'type': 'list',
        'schema': {'type': 'integer', 'nullable': False},
        'required': True,
        'nullable': False,
    },
}
