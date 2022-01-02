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

from polyaxon.config_reader.manager import ConfigManager
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_AUTH,
    CONTEXT_TMP_POLYAXON_PATH,
    CONTEXT_USER_POLYAXON_PATH,
)
from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.api.authentication import AccessTokenConfig


class AuthConfigManager(BaseConfigManager):
    """Manages access token configuration .auth file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_GLOBAL
    CONFIG_FILE_NAME = ".auth"
    CONFIG = AccessTokenConfig

    @classmethod
    def get_config_from_env(cls) -> AccessTokenConfig:
        tmp_path = os.path.join(CONTEXT_TMP_POLYAXON_PATH, cls.CONFIG_FILE_NAME)
        user_path = os.path.join(CONTEXT_USER_POLYAXON_PATH, cls.CONFIG_FILE_NAME)
        auth_config = ConfigManager.read_configs(
            [
                os.environ,
                ConfigSpec(tmp_path, config_type=".json", check_if_exists=False),
                ConfigSpec(user_path, config_type=".json", check_if_exists=False),
                ConfigSpec(
                    CONTEXT_MOUNT_AUTH, config_type=".json", check_if_exists=False
                ),
                {"dummy": "dummy"},
            ]
        )
        return AccessTokenConfig.from_dict(auth_config.data)
