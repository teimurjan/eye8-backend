from src.validation_rules.utils import EMAIL_REGEX, PASSWORD_REGEX

REGISTRATION_VALIDATION_RULES = {
    'name': {'required': True, 'nullable': False, 'empty': False},
    'email': {'required': True, 'nullable': False, 'regex': EMAIL_REGEX},
    'password': {'required': True, 'nullable': False, 'regex': PASSWORD_REGEX}
}
