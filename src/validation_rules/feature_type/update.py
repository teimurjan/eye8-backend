UPDATE_FEATURE_TYPE_VALIDATION_RULES = {
    'names': {
        'type': 'dict',
        'keyschema': {'regex': r'^\d+$'},
        'valueschema': {'type': 'string', 'required': True, 'empty': False, 'nullable': False,'maxlength': 50},
        'required': True,
        'nullable': False,
    },
}
