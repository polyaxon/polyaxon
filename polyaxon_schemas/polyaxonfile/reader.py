# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from collections import Mapping

import numpy as np
import six
import yaml

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.utils import deep_update


def read(config_values):
    """Reads an ordered list of configuration values and deep merge the values in reverse order."""
    if not config_values:
        return None

    if not isinstance(config_values, (np.ndarray, list, tuple)):
        config_values = [config_values]

    config = {}
    for config_value in config_values:
        if not isinstance(config_value, (Mapping, six.string_types)):
            raise PolyaxonConfigurationError(
                "Expects Mapping, string, or list of Mapping/string instances, "
                "received {} instead".format(type(config_value)))

        if isinstance(config_value, Mapping):
            config = deep_update(config, config_value)
        elif os.path.isfile(config_value):
            config = deep_update(config, _read_from_file(config_value))
        else:
            PolyaxonConfigurationError('Cannot read config_value: `{}`'.format(config_value))
    return config


def _read_from_file(f_path):
    _, ext = os.path.splitext(f_path)
    if ext in ('.yml', '.yaml'):
        return _read_from_yml(f_path)
    elif ext == '.json':
        return _read_from_json(f_path)
    raise PolyaxonConfigurationError(
        "Expects a file with extension: `.yml`, `.yaml`, or `json`, "
        "received instead `{}`".format(ext))


def _read_from_yml(f_path):
    with open(f_path) as f:
        f_config = yaml.safe_load(f)
        return f_config


def _read_from_json(f_path):
    try:
        return json.loads(open(f_path).read())
    except ValueError as e:
        raise PolyaxonConfigurationError(e)
