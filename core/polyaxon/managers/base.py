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

from collections import Mapping

import ujson

from polyaxon.containers.contexts import polyaxon_user_path
from polyaxon.logger import logger
from polyaxon.schemas.base import BaseConfig


class BaseConfigManager(object):
    """Base class for managing a configuration file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = False
    CONFIG_PATH = None
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
                logger.error("Could not create config directory `%s`", dir_path)

    @classmethod
    def get_config_filepath(cls, create=True):
        if not cls.IS_GLOBAL:
            # local to this directory
            base_path = os.path.join(".")
            if cls.IS_POLYAXON_DIR:
                # Add it to the current "./.polyaxon"
                base_path = os.path.join(base_path, ".polyaxon")
                if create:
                    cls._create_dir(base_path)
        elif cls.CONFIG_PATH:  # Custom path
            base_path = cls.CONFIG_PATH
        else:
            base_path = polyaxon_user_path()
            if create:
                cls._create_dir(base_path)

        return os.path.join(base_path, cls.CONFIG_FILE_NAME)

    @classmethod
    def init_config(cls):
        config = cls.get_config()
        cls.set_config(config, init=True)

    @classmethod
    def is_initialized(cls):
        config_filepath = cls.get_config_filepath(False)
        return os.path.isfile(config_filepath)

    @classmethod
    def set_config(cls, config, init=False):
        config_filepath = cls.get_config_filepath()

        if os.path.isfile(config_filepath) and init:
            logger.debug(
                "%s file already present at %s", cls.CONFIG_FILE_NAME, config_filepath
            )
            return

        with open(config_filepath, "w") as config_file:
            if hasattr(config, "to_dict"):
                logger.debug(
                    "Setting %s in the file %s", config.to_dict(), cls.CONFIG_FILE_NAME
                )
                config_file.write(ujson.dumps(config.to_dict()))
            elif isinstance(config, Mapping):
                config_file.write(ujson.dumps(config))
            else:
                logger.debug("Setting %s in the file %s", config, cls.CONFIG_FILE_NAME)
                config_file.write(config)

    @classmethod
    def get_config(cls):
        if not cls.is_initialized():
            return None

        config_filepath = cls.get_config_filepath()
        with open(config_filepath, "r") as config_file:
            config_str = config_file.read()
        if issubclass(cls.CONFIG, BaseConfig):
            return cls.CONFIG.from_dict(ujson.loads(config_str))
        return cls.CONFIG(**ujson.loads(config_str))

    @classmethod
    def get_config_or_default(cls):
        if not cls.is_initialized():
            return cls.CONFIG()  # pylint:disable=not-callable

        return cls.get_config()

    @classmethod
    def get_config_from_env(cls, **kwargs):
        raise NotImplementedError

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
        config_filepath = cls.get_config_filepath()

        if not os.path.isfile(config_filepath):
            return

        os.remove(config_filepath)
