import pytz

from datetime import date, datetime, timedelta

from django.conf import settings

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


class DateTimeFormatterException(Exception):
    pass


class DateTimeFormatter(object):
    """
    The `DateTimeFormatter` class implements a utility used to create
    timestamps from strings and vice-versa.
    """
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATETIME_HOUR_FORMAT = '%Y-%m-%d %H:%M'

    @classmethod
    def format_date(cls, timestamp):
        """
        Creates a string representing the date information provided by the
        given `timestamp` object.
        """
        if not timestamp:
            raise DateTimeFormatterException('timestamp must a valid string {}'.format(timestamp))

        return timestamp.strftime(cls.DATE_FORMAT)

    @classmethod
    def format_datetime(cls, timestamp):
        """
        Creates a string representing the date and time information provided by
        the given `timestamp` object.
        """
        if not timestamp:
            raise DateTimeFormatterException('timestamp must a valid string {}'.format(timestamp))

        return timestamp.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def extract_date(cls, date_str):
        """
        Tries to extract a `datetime` object from the given string, expecting
        date information only.

        Raises `DateTimeFormatterException` if the extraction fails.
        """
        if not date_str:
            raise DateTimeFormatterException('date_str must a valid string {}.'.format(date_str))

        try:
            return cls._extract_timestamp(date_str, cls.DATE_FORMAT)
        except (TypeError, ValueError):
            raise DateTimeFormatterException('Invalid date string {}.'.format(date_str))

    @classmethod
    def extract_datetime(cls, datetime_str):
        """
        Tries to extract a `datetime` object from the given string, including
        time information.

        Raises `DateTimeFormatterException` if the extraction fails.
        """
        if not datetime_str:
            raise DateTimeFormatterException('datetime_str must a valid string')

        try:
            return cls._extract_timestamp(datetime_str, cls.DATETIME_FORMAT)
        except (TypeError, ValueError):
            raise DateTimeFormatterException('Invalid datetime string {}.'.format(datetime_str))

    @classmethod
    def extract_datetime_hour(cls, datetime_str):
        """
        Tries to extract a `datetime` object from the given string, including only hours.

        Raises `DateTimeFormatterException` if the extraction fails.
        """
        if not datetime_str:
            raise DateTimeFormatterException('datetime_str must a valid string')

        try:
            return cls._extract_timestamp(datetime_str, cls.DATETIME_HOUR_FORMAT)
        except (TypeError, ValueError):
            raise DateTimeFormatterException('Invalid datetime string {}.'.format(datetime_str))

    @classmethod
    def extract(cls, timestamp_str):
        """
        Tries to extract a `datetime` object from the given string. First the
        datetime format is tried, if it fails, the date format is used for
        extraction.

        Raises `DateTimeFormatterException` if the extraction fails.
        """
        if not timestamp_str:
            raise DateTimeFormatterException(
                'timestamp_str must a valid string {}'.format(timestamp_str))

        if isinstance(timestamp_str, (date, datetime)):
            return timestamp_str

        try:
            return cls.extract_datetime(timestamp_str)
        except DateTimeFormatterException:
            pass

        try:
            return cls.extract_datetime_hour(timestamp_str)
        except DateTimeFormatterException:
            pass

        try:
            return cls.extract_date(timestamp_str)
        except DateTimeFormatterException as e:
            raise DateTimeFormatterException(e)

    @staticmethod
    def _extract_timestamp(timestamp_str, dt_format):
        timestamp = datetime.strptime(timestamp_str, dt_format)
        timestamp = timestamp.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return timestamp
