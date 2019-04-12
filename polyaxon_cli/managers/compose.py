# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.managers.base import BaseConfigManager


class ComposeConfigManager(BaseConfigManager):
    """Manages access cli configuration .polyaxoncli file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.compose/.env'
    FREQUENCY = 3

    @classmethod
    def get_config_file_path(cls, create=True):
        path = super(ComposeConfigManager, cls).get_config_file_path(create=create)
        values = path.split('/')[:-1]
        cls._create_dir('/'.join(values))
        return path
