import pytz

from datetime import datetime, timedelta

epoch = datetime(1970, 1, 1, tzinfo=pytz.utc)


def to_timestamp(value):
    """Convert a time zone aware datetime to a POSIX timestamp (with fractional component.)"""
    return (value - epoch).total_seconds()


def to_datetime(value):
    """Convert a POSIX timestamp to a time zone aware datetime.

    The timestamp value must be a numeric type (either a integer or float,
    since it may contain a fractional component.)
    """
    return epoch + timedelta(seconds=value)
