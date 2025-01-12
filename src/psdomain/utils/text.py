import re
import unicodedata


def slugify(value, allow_unicode=False):
    """
    Convert a string to a URL-friendly slug.
    """
    # Normalize the string to Unicode format
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

    # Replace non-alphanumeric characters with hyphens
    value = re.sub(r'[^\w\s-]', '', value.lower())

    # Replace whitespace or repeated hyphens with a single hyphen
    return re.sub(r'[-\s]+', '-', value).strip('-')
