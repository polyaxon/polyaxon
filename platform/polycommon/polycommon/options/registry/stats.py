#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from django.conf import settings

from polyaxon import types
from polycommon.options import option_namespaces, option_subjects
from polycommon.options.cache import LONG_CACHE_TTL
from polycommon.options.option import (
    NAMESPACE_DB_OPTION_MARKER,
    Option,
    OptionScope,
    OptionStores,
)

STATS_DEFAULT_PREFIX = "{}{}{}".format(
    option_namespaces.STATS, NAMESPACE_DB_OPTION_MARKER, option_subjects.DEFAULT_PREFIX
)

OPTIONS = {STATS_DEFAULT_PREFIX}


class StatsDefaultPrefix(Option):
    key = STATS_DEFAULT_PREFIX
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    typing = types.STR
    store = OptionStores(settings.STORE_OPTION)
    default = None
    options = None
    cache_ttl = LONG_CACHE_TTL
