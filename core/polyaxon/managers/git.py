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

from polyaxon.managers.base import BaseConfigManager
from polyaxon.polyflow import V1Init


class GitConfigManager(BaseConfigManager):
    """Manages access token configuration .auth file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_LOCAL
    CONFIG_FILE_NAME = "polyaxongit.yaml"
    CONFIG = V1Init

    @classmethod
    def get_config_from_env(cls):
        pass
