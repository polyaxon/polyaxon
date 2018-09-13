# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import six
import yaml

from collections import Mapping
from yaml.scanner import ScannerError  # noqa

from rhea.exceptions import RheaError
from rhea.utils import deep_update, to_list


def read(config_values):
    """Reads an ordered list of configuration values and deep merge the values in reverse order."""
    if not config_values:
        raise RheaError('Cannot read config_value: `{}`'.format(config_values))

    config_values = to_list(config_values)

    config = {}
    for config_value in config_values:
        if not isinstance(config_value, (Mapping, six.string_types)):
            raise RheaError(
                "Expects Mapping, string, or list of Mapping/string instances, "
                "received {} instead".format(type(config_value)))

        if isinstance(config_value, Mapping):
            config_results = config_value
        elif os.path.isfile(config_value):
            config_results = _read_from_file(config_value)
        else:
            # try reading a stream of yaml or json
            try:
                config_results = _read_from_stream(config_value)
            except ScannerError:
                raise RheaError(
                    'Received non valid yaml stream: `{}`'.format(config_value))

        if config_results and isinstance(config_results, Mapping):
            config = deep_update(config, config_results)
        else:
            raise RheaError('Cannot read config_value: `{}`'.format(config_value))

    return config


def _read_from_stream(stream):
    results = _read_from_yml(stream, is_stream=True)
    if not results:
        results = _read_from_json(stream, is_stream=True)
    return results


def _read_from_file(f_path):
    _, ext = os.path.splitext(f_path)
    if ext in ('.yml', '.yaml'):
        return _read_from_yml(f_path)
    elif ext == '.json':
        return _read_from_json(f_path)
    raise RheaError(
        "Expects a file with extension: `.yml`, `.yaml`, or `json`, "
        "received instead `{}`".format(ext))


def _read_from_yml(f_path, is_stream=False):
    if is_stream:
        return yaml.safe_load(f_path)
    with open(f_path) as f:
        return yaml.safe_load(f)


def _read_from_json(f_path, is_stream=False):
    if is_stream:
        try:
            return json.loads(f_path)
        except ValueError as e:
            raise RheaError(e)
    try:
        return json.loads(open(f_path).read())
    except ValueError as e:
        raise RheaError(e)
