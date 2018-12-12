from datetime import timedelta

from django.utils.timezone import now


def get_date_check(days):
    return now() - timedelta(days=days)
