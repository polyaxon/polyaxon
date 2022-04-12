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

from polycommon.config_manager import ConfigManager


def set_encryption(context, config: ConfigManager):
    context["ENCRYPTION_KEY"] = config.get_string(
        "POLYAXON_ENCRYPTION_KEY", is_optional=True
    )
    context["ENCRYPTION_SECRET"] = config.get_string(
        "POLYAXON_ENCRYPTION_SECRET", is_optional=True
    )
    context["ENCRYPTION_BACKEND"] = config.get_string(
        "POLYAXON_ENCRYPTION_BACKEND", is_optional=True
    )
