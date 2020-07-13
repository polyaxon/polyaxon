#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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
from polycommon.options.cache import LONG_CACHE_TTL
from polycommon.options.option import Option, OptionScope, OptionStores

LOGGING = "LOGGING"
DEBUG = "DEBUG"
PROTOCOL = "PROTOCOL"
CELERY_BROKER_BACKEND = "CELERY_BROKER_BACKEND"
CELERY_BROKER_URL = "CELERY_BROKER_URL"
SECRET_INTERNAL_TOKEN = "SECRET_INTERNAL_TOKEN"  # noqa
HEALTH_CHECK_WORKER_TIMEOUT = "HEALTH_CHECK_WORKER_TIMEOUT"
SCHEDULER_ENABLED = "SCHEDULER_ENABLED"
UI_ADMIN_ENABLED = "UI_ADMIN_ENABLED"
UI_OFFLINE = "UI_OFFLINE"
UI_ENABLED = "UI_ENABLED"

OPTIONS = {
    LOGGING,
    DEBUG,
    PROTOCOL,
    CELERY_BROKER_BACKEND,
    CELERY_BROKER_URL,
    SECRET_INTERNAL_TOKEN,
    HEALTH_CHECK_WORKER_TIMEOUT,
    SCHEDULER_ENABLED,
    UI_ADMIN_ENABLED,
    UI_OFFLINE,
    UI_ENABLED,
}


class Logging(Option):
    key = LOGGING
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.DICT
    default = None
    options = None


class Debug(Option):
    key = DEBUG
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.DICT
    default = None
    options = None


class Protocol(Option):
    key = PROTOCOL
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class CeleryBrokerBackend(Option):
    key = CELERY_BROKER_BACKEND
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class CeleryBrokerUrl(Option):
    key = CELERY_BROKER_URL
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class SecretInternalToken(Option):
    key = SECRET_INTERNAL_TOKEN
    scope = OptionScope.GLOBAL
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class HealthCheckWorkerTimeout(Option):
    key = HEALTH_CHECK_WORKER_TIMEOUT
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores(settings.STORE_OPTION)
    typing = types.INT
    default = 4
    options = None
    cache_ttl = LONG_CACHE_TTL


class SchedulerEnabled(Option):
    key = SCHEDULER_ENABLED
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.BOOL
    default = True
    options = None


class UiAdminEnabled(Option):
    key = UI_ADMIN_ENABLED
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.BOOL
    default = True
    options = None


class UiOffline(Option):
    key = UI_OFFLINE
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.BOOL
    default = False
    options = None


class UiEnabled(Option):
    key = UI_ENABLED
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.BOOL
    default = False
    options = None
