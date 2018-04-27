# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils.version import LooseVersion  # pylint:disable=import-error

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.schemas.cli_configuration import CliConfigurationConfig


class CliConfigManager(BaseConfigManager):
    """Manages access cli configuration .polyaxoncli file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.polyaxoncli'
    CONFIG = CliConfigurationConfig
    FREQUENCY = 3

    @classmethod
    def _get_count(cls):
        config = cls.get_config_or_default()
        return config.check_count + 1

    @classmethod
    def reset(cls, check_count=None, current_version=None, min_version=None):
        params = {}
        if check_count is not None:
            params['check_count'] = check_count
        if current_version is not None:
            params['current_version'] = current_version
        if min_version is not None:
            params['min_version'] = min_version

        if params:
            config = cls.CONFIG(**params)
            CliConfigManager.set_config(config=config)

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
