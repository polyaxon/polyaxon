# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from rhea.config import ConfigSpec
from rhea.exceptions import RheaError
from rhea.utils import deep_update, to_list


def read(config_values):
    """Reads an ordered list of configuration values and deep merge the values in reverse order."""
    if not config_values:
        raise RheaError('Cannot read config_value: `{}`'.format(config_values))

    config_values = to_list(config_values)

    config = {}
    for config_value in config_values:
        config_value = ConfigSpec.get_from(value=config_value)
        config_value.check_type()
        config_results = config_value.read()
        if config_results and isinstance(config_results, Mapping):
            config = deep_update(config, config_results)
        elif config_value.check_if_exists:
            raise RheaError('Cannot read config_value: `{}`'.format(config_value))

    return config
