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
from polyaxon.schemas.cli.cli_config import CliConfig
from polyaxon.utils.tz_utils import now


class CliConfigManager(BaseConfigManager):
    """Manages access cli configuration .cli file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_GLOBAL
    CONFIG_FILE_NAME = ".cli"
    CONFIG = CliConfig

    @classmethod
    def reset(
        cls,
        current_version=None,
        installation=None,
        compatibility=None,
        log_handler=None,
        last_check=None,
    ):
        if not any(
            [current_version, installation, compatibility, log_handler, last_check]
        ):
            return
        cli_config = cls.get_config_or_default()
        if current_version is not None:
            cli_config.current_version = current_version
        if installation is not None:
            cli_config.installation = installation
        if compatibility is not None:
            cli_config.compatibility = compatibility
        if log_handler is not None:
            cli_config.log_handler = log_handler
        if last_check is not None:
            cli_config.last_check = cli_config.get_last_check(last_check)

        CliConfigManager.set_config(config=cli_config)
        return cli_config

    @classmethod
    def should_check(cls, interval: int = None):
        config = cls.get_config_or_default()
        should_check = config.should_check(interval=interval)
        if should_check:
            cls.reset(last_check=now())
        return should_check

    @classmethod
    def get_config_from_env(cls):
        pass
