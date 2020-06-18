UPDATE_PROMO_CODE_VALIDATION_RULES = {
    'is_active': {'type': 'boolean', 'required': True, 'nullable': False},
    'disable_on_use': {'type': 'boolean', 'required': True, 'nullable': False},
    'products':  {
        'type': 'list',
        'schema': {'type': 'integer', 'nullable': False},
        'required': True,
        'nullable': False,
    },
}
