# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from polyaxon_cli.logger import logger


class BaseConfigManager(object):
    """Base class for managing a configuration file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = False
    CONFIG_FILE_NAME = None
    CONFIG = None

    @staticmethod
    def _create_dir(dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError:
                # Except permission denied and potential race conditions
                # in multi-threaded environments.
                logger.error('Could not create config directory `%s`', dir_path)

    @classmethod
    def get_config_file_path(cls, create=True):
        if not cls.IS_GLOBAL:
            # local to this directory
            base_path = os.path.join('.')
            if cls.IS_POLYAXON_DIR:
                # Add it to the current "./.polyaxon"
                base_path = os.path.join(base_path, '.polyaxon')
                if create:
                    cls._create_dir(base_path)
        else:
            base_path = os.path.expanduser('~')
            if not os.access(base_path, os.W_OK):
                base_path = '/tmp'

            base_path = os.path.join(base_path, '.polyaxon')
            if create:
                cls._create_dir(base_path)

        return os.path.join(base_path, cls.CONFIG_FILE_NAME)

    @classmethod
    def init_config(cls):
        config = cls.get_config()
        cls.set_config(config, init=True)

    @classmethod
    def is_initialized(cls):
        config_file_path = cls.get_config_file_path(False)
        return os.path.isfile(config_file_path)

    @classmethod
    def set_config(cls, config, init=False):
        config_file_path = cls.get_config_file_path()

        if os.path.isfile(config_file_path) and init:
            logger.debug("%s file already present at %s",
                         cls.CONFIG_FILE_NAME, config_file_path)
            return

        with open(config_file_path, "w") as config_file:
            if hasattr(config, 'to_dict'):
                logger.debug(
                    "Setting %s in the file %s", config.to_dict(), cls.CONFIG_FILE_NAME)
                config_file.write(json.dumps(config.to_dict()))
            else:
                logger.debug(
                    "Setting %s in the file %s", config, cls.CONFIG_FILE_NAME)
                config_file.write(config)

    @classmethod
    def get_config(cls):
        if not cls.is_initialized():
            return None

        config_file_path = cls.get_config_file_path()
        with open(config_file_path, "r") as config_file:
            config_str = config_file.read()
        return cls.CONFIG.from_dict(json.loads(config_str))

    @classmethod
    def get_config_or_default(cls):
        if not cls.is_initialized():
            return cls.CONFIG()  # pylint:disable=not-callable

        return cls.get_config()

    @classmethod
    def get_value(cls, key):
        config = cls.get_config()
        if config:
            if hasattr(config, key):
                return getattr(config, key)
            else:
                logger.warning("Config `%s` has no key `%s`", cls.CONFIG.__name__, key)

        return None

    @classmethod
    def purge(cls):
        config_file_path = cls.get_config_file_path()

        if not os.path.isfile(config_file_path):
            return

        os.remove(config_file_path)
