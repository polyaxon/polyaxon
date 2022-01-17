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

import pytz

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

try:
    from django.utils.timezone import now as dj_now  # pylint:disable=import-error
except ImportError:
    dj_now = None


def get_timezone(tz=None):
    from polyaxon import settings

    tz = tz or settings.CLIENT_CONFIG.timezone
    if tz:
        return pytz.timezone(tz)
    return tzlocal()


def now(tzinfo=True, no_micor=False):
    """
    Return an aware or naive datetime.datetime, depending on settings.USE_TZ.
    """
    value = None
    if dj_now:
        try:
            value = dj_now()
        except Exception:  # Improper configuration
            pass
    if not value:
        if tzinfo:
            value = datetime.utcnow().replace(tzinfo=pytz.utc)
        else:
            value = datetime.now()
    if no_micor:
        return value.replace(microsecond=0)
    return value


def local_datetime(datetime_value, tz=None):
    return datetime_value.astimezone(get_timezone(tz))


def get_datetime_from_now(days: int, hours: int = 0, minutes: int = 0) -> datetime:
    return now() - timedelta(days=days, hours=hours, minutes=minutes)
