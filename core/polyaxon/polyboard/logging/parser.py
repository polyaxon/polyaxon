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

import re

from dateutil import parser as dt_parser

# pylint:disable=anomalous-backslash-in-string

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"  # noqa
ISO_DATETIME_REGEX = re.compile(  # noqa
    "([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]"
    "([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\.[0-9]+)?"
    "(([Zz])|([\\+|\\-]([01][0-9]|2[0-3]):[0-5][0-9]))\s?"
)
DATETIME_REGEX = re.compile(  # noqa
    "\d{2}(?:\d{2})?-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\w+\s?"
)


def timestamp_search_regex(regex, log_line):
    log_search = regex.search(log_line)
    if not log_search:
        return log_line, None

    ts = log_search.group()
    ts = dt_parser.parse(ts)

    return re.sub(regex, "", log_line), ts
