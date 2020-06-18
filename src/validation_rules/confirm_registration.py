from src.validation_rules.utils import EMAIL_REGEX, PASSWORD_REGEX

CONFIRM_REGISTRATION_VALIDATION_RULES = {
    'token': {'required': True, 'nullable': False, 'empty': False},
}
