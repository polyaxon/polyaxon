# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from collections import Mapping

import numpy as np
import six
import yaml

from polyaxon_schemas.exceptions import PolyaxonConfigurationError


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
            config = _deep_update(config, config_value)
        elif os.path.isfile(config_value):
            config = _deep_update(config, _read_from_file(config_value))
        else:
            PolyaxonConfigurationError('Cannot read config_value: `{}`'.format(config_value))
    return config


def _deep_update(config, override_config):
    for k, v in six.iteritems(override_config):
        if isinstance(v, Mapping):
            k_config = config.get(k, {})
            if isinstance(k_config, Mapping):
                v_config = _deep_update(k_config, v)
                config[k] = v_config
            else:
                config[k] = v
        else:
            config[k] = override_config[k]
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
