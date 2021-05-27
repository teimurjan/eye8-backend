import secrets
from slugify import slugify


def generate_slug(name: str, with_hash=False):
    slug = slugify(name)
    return f"{slug}-{secrets.token_hex(nbytes=4)}" if with_hash else slug
