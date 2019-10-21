import re
import unicodedata

from django.utils.safestring import mark_safe


def slugify(value: str) -> str:
    """
    Convert spaces/dots to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\.\s-]', '', value).strip()
    return mark_safe(re.sub(r'[-\.\s]+', '-', value))
