from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def normalize_email(email):
    """Normalizes the given email address. In the current implementation it is
    converted to lower case. If the given email is None, an empty string is
    returned.
    """
    email = email or ''
    return email.lower()


def validate_new_email(email):
    """Validates a "new" email address by checking if it is already used by other users."""
    email = normalize_email(email)
    User = get_user_model()
    if User.objects.filter(email=email).exists():
        raise ValidationError('The given email address is already registered.')
