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

import json
import os
import sys
import yaml

from collections import Mapping
from yaml.parser import ParserError  # noqa
from yaml.scanner import ScannerError  # noqa

from polyaxon.exceptions import PolyaxonSchemaError


class ConfigSpec(object):
    def __init__(self, value, config_type=None, check_if_exists=True):
        self.value = value
        self.config_type = config_type
        self.check_if_exists = check_if_exists

    @classmethod
    def get_from(cls, value, config_type=None):
        if isinstance(value, cls):
            return value

        return cls(value=value, config_type=config_type)

    def check_type(self):
        type_check = self.config_type is None and not isinstance(
            self.value, (Mapping, str)
        )
        if type_check:
            raise PolyaxonSchemaError(
                "Expects Mapping, string, or list of Mapping/string instances, "
                "received {} instead".format(type(self.value))
            )

    def read(self):
        if isinstance(self.value, Mapping):
            config_results = self.value
        elif os.path.isfile(self.value):
            config_results = _read_from_file(self.value, self.config_type)
        else:
            # try a python file
            if isinstance(self.value, str) and ".py" in self.value:
                _f_path, _f_module = _get_python_file_def(self.value)
                if _f_path and _f_module:
                    return _read_from_python(_f_path, _f_module)

            # try reading a stream of yaml or json
            try:
                config_results = _read_from_stream(self.value)
            except (ScannerError, ParserError):
                raise PolyaxonSchemaError(
                    "Received an invalid yaml stream: `{}`".format(self.value)
                )
        return config_results


def _read_from_stream(stream):
    results = _read_from_yml(stream, is_stream=True)
    if not results:
        results = _read_from_json(stream, is_stream=True)
    return results


def _get_python_file_def(f_path):
    results = f_path.split(":")
    if len(results) != 2 or not results[1]:
        return None, None

    _f_path = results[0].strip("")
    _module_name = results[1].strip("")
    if not os.path.exists(_f_path):
        raise PolyaxonSchemaError(
            "Received non existing python file: `{}`".format(f_path)
        )
    if not _module_name:
        raise PolyaxonSchemaError(
            "Received an invalid python module: `{}`".format(f_path)
        )
    return _f_path, _module_name


def _import_py_module(f_path, f_module):
    import importlib.util

    spec = importlib.util.spec_from_file_location(f_module, f_path)
    if sys.modules.get(spec.name) and sys.modules[
        spec.name
    ].__file__ == os.path.abspath(spec.origin):
        module = sys.modules[spec.name]
    else:
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return module


def _read_from_python(f_path, f_module):
    f_path = os.path.abspath(f_path)
    file_directory = os.path.dirname(f_path)
    if file_directory not in sys.path:
        sys.path.append(file_directory)

    module_name = os.path.splitext(os.path.basename(f_path))[0]
    module = _import_py_module(f_path, module_name)
    return getattr(module, f_module)


def _read_from_file(f_path, file_type):
    _, ext = os.path.splitext(f_path)
    if ext in (".yml", ".yaml") or file_type in (".yml", ".yaml"):
        return _read_from_yml(f_path)
    elif ext == ".json" or file_type == ".json":
        return _read_from_json(f_path)
    raise PolyaxonSchemaError(
        "Expects a file with extension: `.yml`, `.yaml`, or `json`, "
        "received instead `{}`".format(ext)
    )


def _read_from_yml(f_path, is_stream=False):
    try:
        if is_stream:
            return yaml.safe_load(f_path)
        with open(f_path) as f:
            return yaml.safe_load(f)
    except (ScannerError, ParserError):
        raise PolyaxonSchemaError("Received non valid yaml: `{}`".format(f_path))


def _read_from_json(f_path, is_stream=False):
    if is_stream:
        try:
            return json.loads(f_path)
        except ValueError as e:
            raise PolyaxonSchemaError("Json error: %s" % e) from e
    try:
        return json.loads(open(f_path).read())
    except ValueError as e:
        raise PolyaxonSchemaError("Json error: %s" % e) from e
