# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

CLI_MIN_VERSION = config.get_string('POLYAXON_CLI_MIN_VERSION')
CLI_LATEST_VERSION = config.get_string('POLYAXON_CLI_LATEST_VERSION')
PLATFORM_MIN_VERSION = config.get_string('POLYAXON_PLATFORM_MIN_VERSION')
PLATFORM_LATEST_VERSION = config.get_string('POLYAXON_PLATFORM_LATEST_VERSION')
