UPDATE_PRODUCT_VALIDATION_RULES = {
    'product_type_id': {'type': 'integer', 'required': True, 'nullable': False},
    'images': {
        'type': 'list',
        'schema': {'required': False, 'nullable': True},
        'required': True,
        'nullable': False,
        'minlength': 0,
        'maxlength': 4,
    },
    'price': {'type': 'integer', 'required': True, 'min': 1, 'nullable': False},
    'upc': {'type': 'string', 'required': False, 'nullable': True},
    'discount': {'type': 'integer', 'required': True, 'min': -1, 'max': 100, 'nullable': True},
    'quantity': {'type': 'integer', 'required': True, 'min': 0, 'nullable': False},
    'feature_values': {
        'type': 'list',
        'schema': {'type': 'integer', 'nullable': False},
        'required': True,
        'nullable': False,
    },
}
