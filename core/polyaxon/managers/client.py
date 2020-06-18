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
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.containers.contexts import (
    CONTEXT_TMP_POLYAXON_PATH,
    CONTEXT_USER_POLYAXON_PATH,
)
from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.client_config import ClientConfig


class ClientConfigManager(BaseConfigManager):
    """Manages client configuration .client file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_GLOBAL
    CONFIG_FILE_NAME = ".client"
    CONFIG = ClientConfig

    @classmethod
    def get_config_from_env(cls, **kwargs) -> ClientConfig:
        tmp_path = os.path.join(CONTEXT_TMP_POLYAXON_PATH, cls.CONFIG_FILE_NAME)
        user_path = os.path.join(CONTEXT_USER_POLYAXON_PATH, cls.CONFIG_FILE_NAME)

        config = ConfigManager.read_configs(
            [
                os.environ,
                ConfigSpec(tmp_path, config_type=".json", check_if_exists=False),
                ConfigSpec(user_path, config_type=".json", check_if_exists=False),
            ]
        )
        return ClientConfig.from_dict(config.data)
