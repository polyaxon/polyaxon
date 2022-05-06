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
import os

from polyaxon.config_reader.manager import ConfigManager
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.contexts import paths as ctx_paths
from polyaxon.k8s.namespace import DEFAULT_NAMESPACE
from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.agent_config import AgentConfig, SandboxConfig


class SandboxConfigManager(BaseConfigManager):
    """Manages sandbox configuration .sandbox file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_ALL
    CONFIG_FILE_NAME = ".sandbox"
    CONFIG = SandboxConfig

    @classmethod
    def get_config_from_env(cls):
        config_paths = [
            os.environ,
            {"dummy": "dummy"},
        ]

        config = ConfigManager.read_configs(config_paths)
        return cls.CONFIG.from_dict(config.data)

    @classmethod
    def get_config_or_default(cls) -> SandboxConfig:
        if not cls.is_initialized():
            return cls.get_config_from_env()

        return cls.get_config()


class AgentConfigManager(BaseConfigManager):
    """Manages agent configuration .agent file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_GLOBAL
    CONFIG_FILE_NAME = ".agent"
    CONFIG = AgentConfig

    @classmethod
    def get_config_or_default(cls) -> AgentConfig:
        if not cls.is_initialized():
            return cls.CONFIG(
                namespace=DEFAULT_NAMESPACE, connections=[], secret_resources=[]
            )  # pylint:disable=not-callable

        return cls.get_config()

    @classmethod
    def get_config_from_env(cls) -> AgentConfig:
        tmp_path = os.path.join(
            ctx_paths.CONTEXT_TMP_POLYAXON_PATH, cls.CONFIG_FILE_NAME
        )
        user_path = os.path.join(
            ctx_paths.CONTEXT_USER_POLYAXON_PATH, cls.CONFIG_FILE_NAME
        )

        config_paths = [
            os.environ,
            ConfigSpec(tmp_path, config_type=".json", check_if_exists=False),
            ConfigSpec(user_path, config_type=".json", check_if_exists=False),
            {"dummy": "dummy"},
        ]

        config = ConfigManager.read_configs(config_paths)
        return cls.CONFIG.from_dict(config.data)
