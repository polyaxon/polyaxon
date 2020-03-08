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
import os

from polyaxon.config_reader.manager import ConfigManager
from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.proxies_config import ProxiesConfig


class ProxiesManager(BaseConfigManager):
    """Manages proxies configuration file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = ".proxies"
    CONFIG = ProxiesConfig

    @classmethod
    def get_config_from_env(cls, **kwargs) -> ProxiesConfig:

        config_paths = [os.environ, {"dummy": "dummy"}]

        proxy_config = ConfigManager.read_configs(config_paths)
        return ProxiesConfig.from_dict(proxy_config.data)
