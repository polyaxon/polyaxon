# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.constants import DEFAULT_IGNORE_LIST
from polyaxon_cli.utils.files import matches_glob_list, unix_style_path


class IgnoreManager(BaseConfigManager):
    """Manages .plxignore file in the current directory"""
    IS_GLOBAL = False
    CONFIG_FILE_NAME = '.plxignore'

    @classmethod
    def set_config(cls, config=None):
        config_file_path = cls.get_config_file_path()
        if os.path.isfile(config_file_path):
            logger.debug("{} file already present at {}".format(
                cls.CONFIG_FILE_NAME, config_file_path))
            return

        logger.debug("Setting default {} in the file {}".format(
            cls.CONFIG_FILE_NAME, config_file_path))

        with open(config_file_path, "w") as config_file:
            config_file.write(config or DEFAULT_IGNORE_LIST)

    @classmethod
    def get_config(cls):
        # Remove a preceding '/'. The glob matcher we use will interpret a
        # pattern starging with a '/' as an absolute path, so we remove the
        # '/'. For details on the glob matcher, see:
        # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match
        def trim_slash_prefix(path):
            if path.startswith('/'):
                return line[1:]
            return line

        config_file_path = cls.get_config_file_path()

        if not os.path.isfile(config_file_path):
            return [], []

        ignore_list, white_list = [], []
        with open(config_file_path, "r") as ignore_file:
            for line in ignore_file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('!'):
                    line = line[1:]
                    white_list.append(trim_slash_prefix(line))
                    continue

                # To allow escaping file names that start with !, #, or \,
                # remove the escaping \
                if line.startswith('\\'):
                    line = line[1:]

                ignore_list.append(trim_slash_prefix(line))

        return ignore_list, white_list

    @classmethod
    def get_unignored_file_paths(cls, ignore_list=None, white_list=None):
        config = cls.get_config()
        ignore_list = ignore_list or config[0]
        white_list = white_list or config[1]
        unignored_files = []

        for root, dirs, files in os.walk("."):
            logger.debug("Root:%s, Dirs:%s", root, dirs)

            if cls.ignore_path(unix_style_path(root), ignore_list, white_list):
                dirs[:] = []
                logger.debug("Ignoring directory : %s", root)
                continue

            for file_name in files:
                file_path = unix_style_path(os.path.join(root, file_name))
                if cls.ignore_path(file_path, ignore_list, white_list):
                    logger.debug("Ignoring file : %s", file_name)
                    continue

                unignored_files.append(os.path.join(root, file_name))

        return unignored_files

    @staticmethod
    def ignore_path(path, ignore_list=None, white_list=None):
        """Returns a boolean indicating if a path should be ignored given an
        ignore_list and a white_list of glob patterns.
        """
        ignore_list = ignore_list or []
        white_list = white_list or []
        return matches_glob_list(path, ignore_list) and not matches_glob_list(path, white_list)

    @classmethod
    def get_value(cls, key):
        pass
