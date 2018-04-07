# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from pathlib import PurePath

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.files import unix_style_path


class IgnoreManager(BaseConfigManager):
    """Manages .plxignore file in the current directory"""
    IS_GLOBAL = False
    CONFIG_FILE_NAME = '.polyaxonignore'

    @classmethod
    def init_config(cls):
        cls.set_config(constants.DEFAULT_IGNORE_LIST)

    @staticmethod
    def _is_empty_or_comment(line):
        return not line or line.startswith('#')

    @classmethod
    def _get_whitelisted(cls, line):
        return cls._remove_slash_prefix(line[1:]) if line.startswith('!') else None

    @classmethod
    def _unescape(cls, line):
        """allow escaping file names that start with !, #, or '\' """
        line = line[1:] if line.startswith('\\') else line
        return cls._remove_slash_prefix(line)

    @staticmethod
    def _remove_slash_prefix(line):
        """For details on the glob matcher,
        see: https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.match
        """
        return line[1:] if line.startswith('/') else line

    @classmethod
    def get_config(cls):
        """This is a different config manager since it does not rely on a json object.

        This config return 2 lists representing the ignore_list and white_list of files.
        """
        config_file_path = cls.get_config_file_path()

        if not os.path.isfile(config_file_path):
            return [], []

        ignore_list, white_list = [], []
        with open(config_file_path, "r") as ignore_file:
            for line in ignore_file:
                line = line.strip()
                if cls._is_empty_or_comment(line):
                    continue

                white_list_line = cls._get_whitelisted(line)
                if white_list_line:
                    white_list.append(white_list_line)
                    continue

                ignore_list.append(cls._unescape(line))

        return ignore_list, white_list

    @classmethod
    def get_unignored_file_paths(cls, ignore_list=None, white_list=None):
        config = cls.get_config()
        ignore_list = ignore_list or config[0]
        white_list = white_list or config[1]
        unignored_files = []

        for root, dirs, files in os.walk("."):
            logger.debug("Root:%s, Dirs:%s", root, dirs)

            if cls._ignore_path(unix_style_path(root), ignore_list, white_list):
                dirs[:] = []
                logger.debug("Ignoring directory : %s", root)
                continue

            for file_name in files:
                file_path = unix_style_path(os.path.join(root, file_name))
                if cls._ignore_path(file_path, ignore_list, white_list):
                    logger.debug("Ignoring file : %s", file_name)
                    continue

                unignored_files.append(os.path.join(root, file_name))

        return unignored_files

    @staticmethod
    def _matches_patterns(path, patterns):
        """Given a list of patterns, returns a if a path matches any pattern."""
        for glob in patterns:
            try:
                if PurePath(path).match(glob):
                    return True
            except TypeError:
                pass
        return False

    @classmethod
    def _ignore_path(cls, path, ignore_list=None, white_list=None):
        """Returns a whether a path should be ignored or not."""
        ignore_list = ignore_list or []
        white_list = white_list or []
        return (cls._matches_patterns(path, ignore_list) and
                not cls._matches_patterns(path, white_list))

    @classmethod
    def get_value(cls, key):
        pass
