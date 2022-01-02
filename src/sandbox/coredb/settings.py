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

import django

from django.conf import settings

from polyaxon.config_reader.manager import ConfigManager


def configure():
    AUTH_USER_MODEL = "coredb.User"

    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "coredb.apps.CoreDBConfig",
    ]

    config_values = ["./tests/env_vars/test.json", os.environ]

    config = ConfigManager.read_configs(config_values)
    DEFAULT_DB_ENGINE = "django.db.backends.postgresql"

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        AUTH_USER_MODEL=AUTH_USER_MODEL,
        ROOT_URLCONF="",
        INSTALLED_APPS=INSTALLED_APPS,
        SECRET_KEY="secret",
        CONF_BACKEND="polycommon.conf.service.ConfService",
        K8S_NAMESPACE="test",
        CONF_CHECK_OWNERSHIP=False,
        STORE_OPTION="env",
        OPERATIONS_BACKEND=None,
        AUDITOR_BACKEND=None,
        AUDITOR_EVENTS_TASK=None,
        WORKERS_BACKEND=None,
        EXECUTOR_BACKEND=None,
        WORKERS_SERVICE=None,
        EXECUTOR_SERVICE="coredb.executor",
        DEFAULT_DB_ENGINE="django.db.backends.postgresql",
        DATABASES={
            "default": {
                "ENGINE": config.get_string(
                    "POLYAXON_DB_ENGINE", is_optional=True, default=DEFAULT_DB_ENGINE
                ),
                "NAME": config.get_string("POLYAXON_DB_NAME"),
                "USER": config.get_string("POLYAXON_DB_USER"),
                "PASSWORD": config.get_string("POLYAXON_DB_PASSWORD", is_secret=True),
                "HOST": config.get_string("POLYAXON_DB_HOST"),
                "PORT": config.get_string("POLYAXON_DB_PORT"),
                "ATOMIC_REQUESTS": True,
                "CONN_MAX_AGE": config.get_int(
                    "POLYAXON_DB_CONN_MAX_AGE", is_optional=True, default=None
                ),
            }
        },
    )

    django.setup()
