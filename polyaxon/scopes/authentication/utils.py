from typing import Any

from django.contrib.auth import get_user_model


def is_user(user: Any) -> bool:
    return isinstance(user, get_user_model())
