CREATE_ORDER_VALIDATION_RULES = {
    'items': {
        'type': 'list',
        'schema': {
            'product_id': {'type': 'integer', 'required': True, 'nullable': False},
            'quantity': {'type': 'integer', 'required': True, 'nullable': False}
        },
        'required': True,
        'nullable': False,
    },
    'user_name': {'type': 'string', 'required': True, 'nullable': False},
    'user_phone_number': {'type': 'string', 'required': True, 'nullable': False},
    'user_address': {'type': 'string', 'required': True, 'nullable': False},
    'promo_code': {'type': 'string', 'required': False, 'nullable': True},
}
