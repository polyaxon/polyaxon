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

from typing import Optional, Tuple

from polycommon.config_manager import ConfigManager


def set_apps(
    context,
    config: ConfigManager,
    default_apps: Tuple,
    third_party_apps: Optional[Tuple],
    project_apps: Tuple,
):

    extra_apps = config.get_string(
        "POLYAXON_EXTRA_APPS", is_list=True, is_optional=True
    )
    extra_apps = tuple(extra_apps) if extra_apps else ()

    apps = (
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    )
    third_party_apps = third_party_apps or ()

    context["INSTALLED_APPS"] = (
        apps + third_party_apps + default_apps + extra_apps + project_apps
    )
