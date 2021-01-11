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

from polyaxon.utils.tz_utils import now


def humanize_timesince(start_time):  # pylint:disable=too-many-return-statements
    """Creates a string representation of time since the given `start_time`."""
    if not start_time:
        return start_time

    delta = now() - start_time

    # assumption: negative delta values originate from clock
    #             differences on different app server machines
    if delta.total_seconds() < 0:
        return "a few seconds ago"

    num_years = delta.days // 365
    if num_years > 0:
        return "{} year{} ago".format(
            *((num_years, "s") if num_years > 1 else (num_years, ""))
        )

    num_weeks = delta.days // 7
    if num_weeks > 0:
        return "{} week{} ago".format(
            *((num_weeks, "s") if num_weeks > 1 else (num_weeks, ""))
        )

    num_days = delta.days
    if num_days > 0:
        return "{} day{} ago".format(
            *((num_days, "s") if num_days > 1 else (num_days, ""))
        )

    num_hours = delta.seconds // 3600
    if num_hours > 0:
        return "{} hour{} ago".format(
            *((num_hours, "s") if num_hours > 1 else (num_hours, ""))
        )

    num_minutes = delta.seconds // 60
    if num_minutes > 0:
        return "{} minute{} ago".format(
            *((num_minutes, "s") if num_minutes > 1 else (num_minutes, ""))
        )

    return "a few seconds ago"


def humanize_timedelta(seconds):
    """Creates a string representation of timedelta."""
    hours, remainder = divmod(seconds, 3600)
    days, hours = divmod(hours, 24)
    minutes, seconds = divmod(remainder, 60)

    if days:
        result = "{}d".format(days)
        if hours:
            result += " {}h".format(hours)
        if minutes:
            result += " {}m".format(minutes)
        return result

    if hours:
        result = "{}h".format(hours)
        if minutes:
            result += " {}m".format(minutes)
        return result

    if minutes:
        result = "{}m".format(minutes)
        if seconds:
            result += " {}s".format(seconds)
        return result

    return "{}s".format(seconds)
