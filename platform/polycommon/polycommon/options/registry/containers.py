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

from django.conf import settings

from polyaxon import types
from polyaxon.auxiliaries import (
    V1PolyaxonInitContainer,
    V1PolyaxonSidecarContainer,
    get_default_init_container,
    get_default_sidecar_container,
)
from polycommon.options import option_namespaces, option_subjects
from polycommon.options.cache import MID_FREQUENT_CACHE_TTL
from polycommon.options.option import (
    NAMESPACE_DB_OPTION_MARKER,
    Option,
    OptionScope,
    OptionStores,
)

INIT_CONTAINER = "{}{}{}".format(
    option_namespaces.INIT, NAMESPACE_DB_OPTION_MARKER, option_subjects.CONTAINER
)

SIDECAR_CONTAINER = "{}{}{}".format(
    option_namespaces.SIDECARS, NAMESPACE_DB_OPTION_MARKER, option_subjects.CONTAINER
)

OPTIONS = {SIDECAR_CONTAINER, INIT_CONTAINER}


class PolyaxonInitContainer(Option):
    key = INIT_CONTAINER
    description = "The docker image to use for init container"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    typing = types.STR
    store = OptionStores(settings.STORE_OPTION)
    options = None
    cache_ttl = MID_FREQUENT_CACHE_TTL

    @staticmethod
    def get_default_value():
        return get_default_init_container(schema=False)

    @classmethod
    def _extra_processing(cls, value):
        if not value:
            return value
        V1PolyaxonInitContainer.from_dict(value)
        return value


class PolyaxonSidecarContainer(Option):
    key = SIDECAR_CONTAINER
    description = "Sidecar container definition"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    typing = types.DICT
    store = OptionStores(settings.STORE_OPTION)
    options = None
    cache_ttl = MID_FREQUENT_CACHE_TTL

    @staticmethod
    def get_default_value():
        return get_default_sidecar_container(schema=False)

    @classmethod
    def _extra_processing(cls, value):
        if not value:
            return value
        V1PolyaxonSidecarContainer.from_dict(value)
        return value
