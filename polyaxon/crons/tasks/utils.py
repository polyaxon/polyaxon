from datetime import timedelta
from typing import Any

from django.utils.timezone import now


def get_date_check(days: int) -> Any:
    return now() - timedelta(days=days)
