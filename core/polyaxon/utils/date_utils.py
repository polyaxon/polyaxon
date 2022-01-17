#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import pytz

from datetime import date, datetime, timedelta

from dateutil import parser as dt_parser

from polyaxon.exceptions import PolyaxonDateTimeFormatterException

epoch = datetime(1970, 1, 1, tzinfo=pytz.utc)


def parse_datetime(value):
    if isinstance(value, str):
        return dt_parser.parse(value)
    return value


def to_timestamp(value):
    """
    Convert a time zone aware datetime to a POSIX timestamp (with fractional component.)
    """
    value = parse_datetime(value)
    return (value - epoch).total_seconds()


def to_datetime(value):
    """
    Convert a POSIX timestamp to a time zone aware datetime.

    The timestamp value must be a numeric type (either a integer or float,
    since it may contain a fractional component.)
    """
    return epoch + timedelta(seconds=value)


def path_last_modified(filepath: str) -> datetime:
    return to_datetime(os.stat(filepath).st_mtime)


def file_modified_since(filepath: str, last_time: datetime) -> bool:
    if not last_time:
        return True
    return path_last_modified(filepath) > last_time


def as_timezone(value, timezone):
    return value.astimezone(pytz.timezone(timezone))


class DateTimeFormatter:
    """
    The `DateTimeFormatter` class implements a utility used to create
    timestamps from strings and vice-versa.
    """

    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_HOUR_FORMAT = "%Y-%m-%d %H:%M"

    @classmethod
    def format_date(cls, timestamp):
        """
        Creates a string representing the date information provided by the
        given `timestamp` object.
        """
        if not timestamp:
            raise PolyaxonDateTimeFormatterException(
                "timestamp must a valid string {}".format(timestamp)
            )

        return timestamp.strftime(cls.DATE_FORMAT)

    @classmethod
    def format_datetime(cls, timestamp):
        """
        Creates a string representing the date and time information provided by
        the given `timestamp` object.
        """
        if not timestamp:
            raise PolyaxonDateTimeFormatterException(
                "timestamp must a valid string {}".format(timestamp)
            )

        return timestamp.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def extract_date(cls, date_str, timezone, force_tz: bool = False):
        """
        Tries to extract a `datetime` object from the given string, expecting
        date information only.

        Raises `PolyaxonDateTimeFormatterException` if the extraction fails.
        """
        if not date_str:
            raise PolyaxonDateTimeFormatterException(
                "date_str must a valid string {}.".format(date_str)
            )

        if not timezone:
            raise PolyaxonDateTimeFormatterException(
                "timezone is required, received {}".format(timezone)
            )

        try:
            return cls.extract_iso_timestamp(
                date_str, timezone=timezone, force_tz=force_tz
            )
        except (TypeError, ValueError, AttributeError):
            pass

        try:
            return cls.extract_timestamp(
                date_str, cls.DATE_FORMAT, timezone=timezone, force_tz=force_tz
            )
        except (TypeError, ValueError):
            raise PolyaxonDateTimeFormatterException(
                "Invalid date string {}.".format(date_str)
            )

    @classmethod
    def extract_datetime(cls, datetime_str, timezone, force_tz: bool = False):
        """
        Tries to extract a `datetime` object from the given string, including
        time information.

        Raises `PolyaxonDateTimeFormatterException` if the extraction fails.
        """
        if not datetime_str:
            raise PolyaxonDateTimeFormatterException("datetime_str must a valid string")

        if not timezone:
            raise PolyaxonDateTimeFormatterException(
                "timezone is required, received {}".format(timezone)
            )

        try:
            return cls.extract_iso_timestamp(
                datetime_str, timezone=timezone, force_tz=force_tz
            )
        except (TypeError, ValueError, AttributeError):
            pass

        try:
            return cls.extract_timestamp(
                datetime_str, cls.DATETIME_FORMAT, timezone=timezone, force_tz=force_tz
            )
        except (TypeError, ValueError):
            raise PolyaxonDateTimeFormatterException(
                "Invalid datetime string {}.".format(datetime_str)
            )

    @classmethod
    def extract_datetime_hour(cls, datetime_str, timezone, force_tz: bool = False):
        """
        Tries to extract a `datetime` object from the given string, including only hours.

        Raises `PolyaxonDateTimeFormatterException` if the extraction fails.
        """
        if not datetime_str:
            raise PolyaxonDateTimeFormatterException("datetime_str must a valid string")

        if not timezone:
            raise PolyaxonDateTimeFormatterException(
                "timezone is required, received {}".format(timezone)
            )

        try:
            return cls.extract_iso_timestamp(
                datetime_str, timezone=timezone, force_tz=force_tz
            )
        except (TypeError, ValueError, AttributeError):
            pass

        try:
            return cls.extract_timestamp(
                datetime_str,
                cls.DATETIME_HOUR_FORMAT,
                timezone=timezone,
                force_tz=force_tz,
            )
        except (TypeError, ValueError):
            raise PolyaxonDateTimeFormatterException(
                "Invalid datetime string {}.".format(datetime_str)
            )

    @classmethod
    def extract(cls, timestamp_str, timezone):
        """
        Tries to extract a `datetime` object from the given string. First the
        datetime format is tried, if it fails, the date format is used for
        extraction.

        Raises `PolyaxonDateTimeFormatterException` if the extraction fails.
        """
        if not timestamp_str:
            raise PolyaxonDateTimeFormatterException(
                "timestamp_str must a valid string, received {}".format(timestamp_str)
            )

        if not timezone:
            raise PolyaxonDateTimeFormatterException(
                "timezone is required, received {}".format(timezone)
            )

        if isinstance(timestamp_str, (date, datetime)):
            return timestamp_str

        try:
            return cls.extract_datetime(timestamp_str, timezone=timezone)
        except PolyaxonDateTimeFormatterException:
            pass

        try:
            return cls.extract_datetime_hour(timestamp_str, timezone=timezone)
        except PolyaxonDateTimeFormatterException:
            pass

        # We leave it to raise
        return cls.extract_date(timestamp_str, timezone=timezone)

    @staticmethod
    def extract_iso_timestamp(timestamp_str, timezone, force_tz: bool = False):
        timestamp = datetime.fromisoformat(timestamp_str)
        if not timestamp.tzinfo and timezone:
            timestamp = timestamp.replace(tzinfo=pytz.timezone(timezone))
        if force_tz:
            timestamp = as_timezone(timestamp, timezone)
        return timestamp

    @staticmethod
    def extract_timestamp(timestamp_str, dt_format, timezone, force_tz: bool = False):
        timestamp = datetime.strptime(timestamp_str, dt_format)
        timestamp = timestamp.replace(tzinfo=pytz.timezone(timezone))
        if force_tz:
            timestamp = as_timezone(timestamp, timezone)
        return timestamp
