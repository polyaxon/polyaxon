# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import re

from collections import namedtuple
from pathlib import PurePath

from polyaxon_cli.logger import logger
from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.files import unix_style_path


class Pattern(namedtuple("Pattern", "pattern is_exclude re")):
    @staticmethod
    def create(pattern):
        if pattern[0:1] == '!':
            is_exclude = False
            pattern = pattern[1:]
        else:
            if pattern[0:1] == '\\':
                pattern = pattern[1:]
            is_exclude = True
        return Pattern(pattern=pattern,
                       is_exclude=is_exclude,
                       re=re.compile(translate(pattern), re.IGNORECASE))

    def match(self, path):
        return bool(self.re.match(path))


def translate(pat):
    def _translate_segment():
        # pylint:disable=undefined-loop-variable
        if segment == '*':
            return '[^/]+'
        res = ''
        i, n = 0, len(segment)
        while i < n:
            c = segment[i:i + 1]
            i = i + 1
            if c == '*':
                res += '[^/]*'
            elif c == '?':
                res += '[^/]'
            elif c == '[':
                j = i
                if j < n and segment[j:j + 1] == '!':
                    j = j + 1
                if j < n and segment[j:j + 1] == ']':
                    j = j + 1
                while j < n and segment[j:j + 1] != ']':
                    j = j + 1
                if j >= n:
                    res += '\\['
                else:
                    stuff = segment[i:j].replace('\\', '\\\\')
                    i = j + 1
                    if stuff.startswith('!'):
                        stuff = '^' + stuff[1:]
                    elif stuff.startswith('^'):
                        stuff = '\\' + stuff
                    res += '[' + stuff + ']'
            else:
                res += re.escape(c)
        return res

    res = '(?ms)'

    if '/' not in pat[:-1]:
        res += '(.*/)?'

    if pat.startswith('**/'):
        pat = pat[2:]
        res += '(.*/)?'

    if pat.startswith('/'):
        pat = pat[1:]

    for i, segment in enumerate(pat.split('/')):
        if segment == '**':
            res += '(/.*)?'
            continue
        else:
            res += ((re.escape('/') if i > 0 else '') + _translate_segment())

    if not pat.endswith('/'):
        res += '/?'

    return res + '\\Z'


class IgnoreManager(BaseConfigManager):
    """Manages .plxignore file in the current directory"""
    IS_GLOBAL = False
    CONFIG_FILE_NAME = '.polyaxonignore'

    @staticmethod
    def _is_empty_or_comment(line):
        return not line or line.startswith('#')

    @staticmethod
    def _remove_trailing_spaces(line):
        """Remove trailing spaces unless they are quoted with a backslash."""
        while line.endswith(' ') and not line.endswith('\\ '):
            line = line[:-1]
        return line.replace('\\ ', ' ')

    @classmethod
    def init_config(cls):
        cls.set_config(constants.DEFAULT_IGNORE_LIST, init=True)

    @classmethod
    def find_matching(cls, path, patterns):
        """Yield all matching patterns for path."""
        for pattern in patterns:
            if pattern.match(path):
                yield pattern

    @classmethod
    def is_ignored(cls, path, patterns):
        """Check whether a path is ignored. For directories, include a trailing slash."""
        status = None
        for pattern in cls.find_matching(path, patterns):
            status = pattern.is_exclude
        return status

    @classmethod
    def read_file(cls, ignore_file):
        for line in ignore_file:
            line = line.rstrip('\r\n')

            if cls._is_empty_or_comment(line):
                continue

            yield cls._remove_trailing_spaces(line)

    @classmethod
    def get_patterns(cls, ignore_file):
        return [Pattern.create(line) for line in cls.read_file(ignore_file)]

    @classmethod
    def get_config(cls):
        config_file_path = cls.get_config_file_path()

        if not os.path.isfile(config_file_path):
            return []

        with open(config_file_path, "r") as ignore_file:
            return cls.get_patterns(ignore_file)

    @classmethod
    def get_unignored_file_paths(cls):
        config = cls.get_config()
        unignored_files = []

        for root, dirs, files in os.walk("."):
            logger.debug("Root:%s, Dirs:%s", root, dirs)

            if cls.is_ignored(unix_style_path(root), config):
                dirs[:] = []
                logger.debug("Ignoring directory : %s", root)
                continue

            for file_name in files:
                file_path = unix_style_path(os.path.join(root, file_name))
                if cls.is_ignored(file_path, config):
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
