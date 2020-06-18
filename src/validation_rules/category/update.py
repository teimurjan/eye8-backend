UPDATE_CATEGORY_VALIDATION_RULES = {
    'names': {
        'type': 'dict',
        'keyschema': {'regex': r'^\d+$'},
        'valueschema': {'type': 'string', 'required': True, 'empty': False, 'nullable': False,'maxlength': 50},
        'required': True,
        'nullable': False,
    },
    'parent_category_id': {'type': 'integer', 'nullable': True, 'required': False},
}
