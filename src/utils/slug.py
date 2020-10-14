import secrets
from src.models.intl import IntlText
from slugify import slugify


def is_name_en(name: IntlText):
    return name.language.name == "en"


def generate_slug(entity: IntlText, with_hash=False):
    reliable_name = [name.value for name in entity.names if is_name_en(name)][0]
    slug = slugify(reliable_name)
    return f"{slug}-{secrets.token_hex(nbytes=4)}" if with_hash else slug
