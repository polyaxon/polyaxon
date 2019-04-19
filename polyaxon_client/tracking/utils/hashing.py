from polyaxon_client import settings


def hash_value(value):
    import hashlib

    return hashlib.md5(str(value).encode("utf-8")).hexdigest()[:settings.HASH_LENGTH]
