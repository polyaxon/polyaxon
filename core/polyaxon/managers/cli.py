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

from distutils.version import LooseVersion  # pylint:disable=import-error

from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.cli_config import CliConfigurationConfig


class CliConfigManager(BaseConfigManager):
    """Manages access cli configuration .polyaxoncli file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = ".polyaxoncli"
    CONFIG = CliConfigurationConfig
    FREQUENCY = 3

    @classmethod
    def _get_count(cls):
        config = cls.get_config_or_default()
        return config.check_count + 1

    @classmethod
    def reset(
        cls,
        check_count=None,
        current_version=None,
        server_versions=None,
        log_handler=None,
    ):
        if not any([check_count, current_version, server_versions, log_handler]):
            return
        cli_config = cls.get_config_or_default()
        if check_count is not None:
            cli_config.check_count = check_count
        if current_version is not None:
            cli_config.current_version = current_version
        if server_versions is not None:
            cli_config.server_versions = server_versions
        if log_handler is not None:
            cli_config.log_handler = log_handler

        CliConfigManager.set_config(config=cli_config)
        return cli_config

    @classmethod
    def should_check(cls):
        count = cls._get_count()
        cls.reset(check_count=count)
        if count > cls.FREQUENCY:
            return True

        config = cls.get_config_or_default()
        if config.current_version is None or config.min_version is None:
            return True
        return LooseVersion(config.current_version) < LooseVersion(config.min_version)
