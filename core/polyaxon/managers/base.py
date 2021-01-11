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

from collections.abc import Mapping
from typing import Callable, Optional

import ujson

from polyaxon.containers.contexts import polyaxon_user_path
from polyaxon.logger import logger
from polyaxon.schemas.base import BaseConfig


class BaseConfigManager:
    """Base class for managing a configuration file."""

    VISIBILITY_GLOBAL = "global"
    VISIBILITY_LOCAL = "local"
    VISIBILITY_ALL = "all"
    VISIBILITY_PATH = "path"

    VISIBILITY = None
    IS_POLYAXON_DIR = False
    CONFIG_PATH = None
    CONFIG_FILE_NAME = None
    CONFIG = None

    @classmethod
    def is_global(cls, visibility=None):
        visibility = visibility or cls.VISIBILITY
        return visibility == cls.VISIBILITY_GLOBAL

    @classmethod
    def is_local(cls, visibility=None):
        visibility = visibility or cls.VISIBILITY
        return visibility == cls.VISIBILITY_LOCAL

    @classmethod
    def is_all_visibility(cls, visibility=None):
        visibility = visibility or cls.VISIBILITY
        return visibility == cls.VISIBILITY_ALL

    @classmethod
    def is_path_visibility(cls, visibility=None):
        visibility = visibility or cls.VISIBILITY
        return visibility == cls.VISIBILITY_PATH

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
    def create_config_filepath(cls, visibility=None):
        if cls.is_local(visibility):
            # Local to this directory
            base_path = os.path.join(".")
            if cls.IS_POLYAXON_DIR:
                # Add it to the current "./.polyaxon"
                base_path = os.path.join(base_path, ".polyaxon")
                cls._create_dir(base_path)
        elif cls.CONFIG_PATH:  # Custom path
            pass
        else:  # Handle both global and all cases
            base_path = polyaxon_user_path()
            cls._create_dir(base_path)

    @classmethod
    def get_local_config_path(cls) -> str:
        # local to this directory
        base_path = os.path.join(".")
        if cls.IS_POLYAXON_DIR:
            # Add it to the current "./.polyaxon"
            base_path = os.path.join(base_path, ".polyaxon")
        config_path = os.path.join(base_path, cls.CONFIG_FILE_NAME)
        return config_path

    @staticmethod
    def _get_and_check_path(fct: Callable) -> Optional[str]:
        config_path = fct()
        if config_path and os.path.exists(config_path):
            return config_path
        return None

    @classmethod
    def check_local_config_path(cls) -> Optional[str]:
        return cls._get_and_check_path(cls.get_local_config_path)

    @classmethod
    def get_global_config_path(cls) -> str:
        base_path = polyaxon_user_path()
        config_path = os.path.join(base_path, cls.CONFIG_FILE_NAME)
        return config_path

    @classmethod
    def check_global_config_path(cls) -> Optional[str]:
        return cls._get_and_check_path(cls.get_global_config_path)

    @classmethod
    def get_custom_config_path(cls) -> str:
        config_path = os.path.join(cls.CONFIG_PATH, cls.CONFIG_FILE_NAME)
        return config_path

    @classmethod
    def check_custom_config_path(cls) -> Optional[str]:
        return cls._get_and_check_path(cls.get_custom_config_path)

    @classmethod
    def get_config_filepath(cls, create=True, visibility=None):
        if create:
            cls.create_config_filepath(visibility=visibility)

        if cls.is_local(visibility):
            return cls.get_local_config_path()
        if cls.is_path_visibility(visibility):
            return cls.get_custom_config_path()
        if cls.is_global(visibility):
            return cls.get_global_config_path()
        if cls.is_all_visibility(visibility):
            config_path = cls.check_local_config_path()
            if config_path:
                return config_path
            return cls.get_global_config_path()

        return None

    @classmethod
    def init_config(cls, visibility=None):
        config = cls.get_config()
        cls.set_config(config, init=True, visibility=visibility)

    @classmethod
    def is_locally_initialized(cls):
        return cls.check_local_config_path()

    @classmethod
    def is_initialized(cls):
        config_filepath = cls.get_config_filepath(create=False)
        return config_filepath and os.path.isfile(config_filepath)

    @classmethod
    def set_config(cls, config, init=False, visibility=None):
        config_filepath = cls.get_config_filepath(visibility=visibility)

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
    def purge(cls, visibility=None):
        def _purge():
            if config_filepath and os.path.isfile(config_filepath):
                os.remove(config_filepath)

        if cls.is_all_visibility():
            if visibility:
                config_filepath = cls.get_config_filepath(
                    create=False, visibility=visibility
                )
                _purge()
            else:
                config_filepath = cls.get_config_filepath(
                    create=False, visibility=cls.VISIBILITY_LOCAL
                )
                _purge()
                config_filepath = cls.get_config_filepath(
                    create=False, visibility=cls.VISIBILITY_GLOBAL
                )
                _purge()
        else:
            config_filepath = cls.get_config_filepath(create=False)
            _purge()
