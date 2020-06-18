UPDATE_FEATURE_VALUE_VALIDATION_RULES = {
    'names': {
        'type': 'dict',
        'keyschema': {'regex': r'^\d+$'},
        'valueschema': {'type': 'string', 'required': True, 'empty': False, 'nullable': False,'maxlength': 50},
        'required': True,
        'nullable': False,
    },
    'feature_type_id': {'type': 'integer', 'required': True, 'nullable': False},
}
