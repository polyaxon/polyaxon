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

from polycommon.config_manager import ConfigManager


def set_core(context, config: ConfigManager):
    context["DEBUG"] = config.is_debug_mode
    context["POLYAXON_SERVICE"] = config.service
    context["POLYAXON_ENVIRONMENT"] = config.env
    context["CHART_VERSION"] = config.chart_version
    context["SCHEDULER_ENABLED"] = config.scheduler_enabled
    context["ORGANIZATION_KEY"] = config.get_string(
        "POLYAXON_ORGANIZATION_KEY", is_optional=True
    )
    context["K8S_NAMESPACE"] = config.namespace

    context["FILE_UPLOAD_PERMISSIONS"] = 0o644

    context["WSGI_APPLICATION"] = "polyconf.wsgi.application"
    context["TIME_ZONE"] = config.timezone
    context["LANGUAGE_CODE"] = "en"
    context["LANGUAGES"] = (("en", u"English"),)

    context["USE_I18N"] = True
    context["USE_L10N"] = True
    context["USE_TZ"] = True

    context["INTERNAL_IPS"] = ("127.0.0.1",)
    context["APPEND_SLASH"] = True

    context["ROOT_URLCONF"] = ""

    db_engine = "django.db.backends.postgresql"
    context["DEFAULT_DB_ENGINE"] = db_engine
    context["DATABASES"] = {
        "default": {
            "ENGINE": config.get_string(
                "POLYAXON_DB_ENGINE", is_optional=True, default=db_engine
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
    }
