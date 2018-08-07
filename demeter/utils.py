import datetime
from decimal import Decimal


def is_protected_type(obj):
    """
    A check for preserving a type as-is when passed to force_text(strings_only=True).
    """
    return isinstance(obj, (
        type(None), int, float, Decimal, datetime.datetime, datetime.date, datetime.time,))


def force_bytes(value, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Resolve any value to strings.

    If `strings_only` is True, skip protected objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(value, bytes):
        if encoding == 'utf-8':
            return value
        else:
            return value.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(value):
        return value
    if isinstance(value, memoryview):
        return bytes(value)
    else:
        return value.encode(encoding, errors)
