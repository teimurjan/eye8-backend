import secrets
from slugify import slugify

def is_name_en(name):
  if name.language is not None:
    return name.language.name == 'en'
  
  return name.language_id == 1

def generate_slug(entity, with_hash=False):
    reliable_name = [
        name.value for name in entity.names if is_name_en(name)][0]
    slug = slugify(reliable_name)
    return f'{slug}-{secrets.token_hex(nbytes=4)}' if with_hash else slug
