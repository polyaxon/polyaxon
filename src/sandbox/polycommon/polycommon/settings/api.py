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
from typing import List

from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_PLATFORM_HOST,
    POLYAXON_KEYS_UI_ADMIN_ENABLED,
    POLYAXON_KEYS_UI_ASSETS_VERSION,
    POLYAXON_KEYS_UI_BASE_URL,
    POLYAXON_KEYS_UI_ENABLED,
    POLYAXON_KEYS_UI_OFFLINE,
)
from polycommon.config_manager import ConfigManager


def set_api(context, config: ConfigManager, processors: List[str] = None):
    context["ROOT_URLCONF"] = "polyconf.urls"
    platform_host = config.get_string(POLYAXON_KEYS_PLATFORM_HOST, is_optional=True)
    context["PLATFORM_HOST"] = platform_host

    def get_allowed_hosts():
        allowed_hosts = config.get_string(
            "POLYAXON_ALLOWED_HOSTS", is_optional=True, is_list=True, default=["*"]
        )  # type: list
        if platform_host:
            allowed_hosts.append(platform_host)
        if ".polyaxon.com" not in allowed_hosts:
            allowed_hosts.append(".polyaxon.com")
        pod_ip = config.get_string("POLYAXON_POD_IP", is_optional=True)
        if pod_ip:
            allowed_hosts.append(pod_ip)
        host_ip = config.get_string("POLYAXON_HOST_IP", is_optional=True)
        if host_ip:
            host_cidr = ".".join(host_ip.split(".")[:-1])
            allowed_hosts += ["{}.{}".format(host_cidr, i) for i in range(255)]

        return allowed_hosts

    context["ALLOWED_HOSTS"] = get_allowed_hosts()

    processors = processors or []
    processors = [
        "django.contrib.auth.context_processors.auth",
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.template.context_processors.media",
        "django.template.context_processors.static",
        "django.template.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        "polycommon.settings.context_processors.version",
        "polycommon.settings.context_processors.ui_assets_version",
        "polycommon.settings.context_processors.ui_base_url",
        "polycommon.settings.context_processors.ui_offline",
        "polycommon.settings.context_processors.ui_enabled",
    ] + processors

    context["FRONTEND_DEBUG"] = config.get_boolean("POLYAXON_FRONTEND_DEBUG")

    template_debug = (
        config.get_boolean("DJANGO_TEMPLATE_DEBUG", is_optional=True)
        or config.is_debug_mode
    )
    context["UI_ADMIN_ENABLED"] = config.get_boolean(
        POLYAXON_KEYS_UI_ADMIN_ENABLED, is_optional=True, default=False
    )
    base_url = config.get_string(POLYAXON_KEYS_UI_BASE_URL, is_optional=True)
    if base_url:
        context["UI_BASE_URL"] = base_url
        context["FORCE_SCRIPT_NAME"] = base_url
    else:
        context["UI_BASE_URL"] = "/"
    context["UI_ASSETS_VERSION"] = config.get_string(
        POLYAXON_KEYS_UI_ASSETS_VERSION, is_optional=True, default=""
    )
    context["UI_OFFLINE"] = config.get_boolean(
        POLYAXON_KEYS_UI_OFFLINE, is_optional=True, default=False
    )
    context["UI_ENABLED"] = config.get_boolean(
        POLYAXON_KEYS_UI_ENABLED, is_optional=True, default=True
    )
    context["TEMPLATES_DEBUG"] = template_debug
    context["LIST_TEMPLATE_CONTEXT_PROCESSORS"] = processors
    context["TEMPLATES"] = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {"debug": template_debug, "context_processors": processors},
        }
    ]
