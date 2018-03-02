# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.schemas.cli_configuration import CliConfigurationConfig


class CliConfigManager(BaseConfigManager):
    """Manages access cli configuration .polyaxoncli file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.polyaxoncli'
    CONFIG = CliConfigurationConfig
    FREQUENCY = 5

    @classmethod
    def _get_count(cls):
        config = cls.get_config_or_default()
        return config.check_count + 1

    @classmethod
    def _set_new_count(cls, count):
        if count > cls.FREQUENCY:
            count = 0
        config = cls.CONFIG(check_count=count)
        cls.set_config(config=config)

    @classmethod
    def should_check(cls):
        count = cls._get_count()
        cls._set_new_count(count)
        return count > cls.FREQUENCY
