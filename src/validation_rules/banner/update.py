UPDATE_BANNER_VALIDATION_RULES = {
    'texts': {
        'type': 'dict',
        'keyschema': {'regex': r'^\d+$'},
        'valueschema': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
        'required': True,
        'nullable': False,
    },
    'image': {'required': True, 'nullable': False},
    'link': {'required': False, 'nullable': True},
    'text_color': {'required': False, 'nullable': True},
    'link_texts': {
        'type': 'dict',
        'keyschema': {'regex': r'^\d+$'},
        'valueschema': {'type': 'string', 'required': True, 'empty': False, 'nullable': False,'maxlength': 50},
        'required': True,
        'nullable': False,
    },
    'text_top_offset': {'type': 'integer', 'required': False, 'nullable': True},
    'text_bottom_offset': {'type': 'integer', 'required': False, 'nullable': True},
    'text_left_offset': {'type': 'integer', 'required': False, 'nullable': True},
    'text_right_offset': {'type': 'integer', 'required': False, 'nullable': True},
}
