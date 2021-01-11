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

import json
import os
import sys
import yaml

from collections.abc import Mapping
from requests import HTTPError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from polyaxon_sdk import ApiException

from polyaxon.config_reader.utils import deep_update
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_PUBLIC_REGISTRY,
    POLYAXON_KEYS_USE_GIT_REGISTRY,
)
from polyaxon.exceptions import PolyaxonClientException, PolyaxonSchemaError
from polyaxon.utils.list_utils import to_list


class ConfigSpec:
    def __init__(self, value, config_type=None, check_if_exists=True):
        self.value = value
        self.config_type = config_type
        self.check_if_exists = check_if_exists

    @classmethod
    def get_from(cls, value: object, config_type: object = None) -> "ConfigSpec":
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
            return self.value

        # try a python file
        if isinstance(self.value, str) and (
            self.config_type == ".py" or ".py" in self.value
        ):
            _f_path, _f_module = _get_python_file_def(self.value)
            if _f_path and _f_module:
                return _read_from_python(_f_path, _f_module)

        if os.path.isfile(self.value):
            return _read_from_file(self.value, self.config_type)

        # try reading a stream of yaml or json
        if not self.config_type or self.config_type in (".json", ".yml", ".yaml"):
            try:
                return _read_from_stream(self.value)
            except (ScannerError, ParserError):
                raise PolyaxonSchemaError(
                    "Received an invalid yaml stream: `{}`".format(self.value)
                )

        if self.config_type == "url":
            return _read_from_url(self.value)

        if self.config_type == "hub":
            if os.environ.get(POLYAXON_KEYS_USE_GIT_REGISTRY, False):
                return _read_from_public_hub(self.value)
            return _read_from_polyaxon_hub(self.value)

        raise PolyaxonSchemaError(
            "Received an invalid configuration: `{}`".format(self.value)
        )

    @classmethod
    def read_from(cls, config_values, config_type=None):
        """
        Reads an ordered list of configuration values and
        deep merge the values in reverse order.
        """
        if not config_values:
            raise PolyaxonSchemaError(
                "Cannot read config_value: `{}`".format(config_values)
            )

        config_values = to_list(config_values, check_none=True)

        config = {}
        for config_value in config_values:
            config_value = ConfigSpec.get_from(
                value=config_value, config_type=config_type
            )
            config_value.check_type()
            config_results = config_value.read()
            if config_results and isinstance(config_results, Mapping):
                config = deep_update(config, config_results)
            elif config_value.check_if_exists:
                raise PolyaxonSchemaError(
                    "Cannot read config_value: `{}`".format(config_value.value)
                )

        return config


def _read_from_url(url: str):
    from polyaxon.utils.requests_utils import safe_request

    resp = safe_request(url)
    resp.raise_for_status()
    return _read_from_stream(resp.content.decode())


def get_default_registry():
    return os.environ.get(
        POLYAXON_KEYS_PUBLIC_REGISTRY,
        "https://raw.githubusercontent.com/polyaxon/polyaxon-hub/master",
    )


def _read_from_public_hub(hub: str):
    hub_values = hub.split(":")
    if len(hub_values) > 2:
        raise PolyaxonSchemaError("Received an invalid hub reference: `{}`".format(hub))
    if len(hub_values) == 2:
        hub_name, version = hub_values
    else:
        hub_name, version = hub_values[0], "latest"
    version = version or "latest"
    registry = get_default_registry()
    url = "{}/{}/{}.yaml".format(registry, hub_name, version)
    try:
        return _read_from_url(url)
    except HTTPError as e:
        if e.response.status_code == 404:
            raise PolyaxonClientException(
                "Component `{}` was not found, "
                "please check that the name and tag are valid".format(hub)
            )
        raise PolyaxonClientException(
            "Component `{}` could not be fetched, "
            "an error was encountered".format(hub, e)
        )


def _read_from_polyaxon_hub(hub: str):
    from polyaxon.client import PolyaxonClient
    from polyaxon.constants import DEFAULT_HUB, NO_AUTH
    from polyaxon.env_vars.getters import get_component_info
    from polyaxon.schemas.cli.client_config import ClientConfig

    owner, component, version = get_component_info(hub)

    try:
        if owner == DEFAULT_HUB:
            config = ClientConfig()
            client = PolyaxonClient(
                config=config,
                token=NO_AUTH,
            )
        else:
            client = PolyaxonClient()
        response = client.component_hub_v1.get_component_version(
            owner, component, version
        )
        return _read_from_stream(response.content)
    except (ApiException, HTTPError) as e:
        raise PolyaxonClientException(
            "Component `{}` could not be fetched, "
            "an error was encountered".format(hub, e)
        )


def _read_from_stream(stream):
    results = _read_from_yml(stream, is_stream=True)
    if not results:
        results = _read_from_json(stream, is_stream=True)
    return results


def _get_python_file_def(f_path):
    if not isinstance(f_path, str) or ".py" not in f_path:
        return None, None
    results = f_path.split(":")

    if len(results) == 1:  # Default case
        return f_path, "main"

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
    elif ext == ".py" or file_type == ".py":
        _f_path, _f_module = _get_python_file_def(f_path)
        if _f_path and _f_module:
            return _read_from_python(_f_path, _f_module)
    raise PolyaxonSchemaError(
        "Expects a file with extension: `.yml`, `.yaml`, `.py`, or `json`, "
        "received instead `{}`".format(ext)
    )


def _read_from_yml(f_path, is_stream=False):
    try:
        if is_stream:
            return yaml.safe_load(f_path)
        with open(f_path) as f:
            return yaml.safe_load(f)
    except (ScannerError, ParserError) as e:
        raise PolyaxonSchemaError(
            "Received non valid yaml: `%s`.\n" "Yaml error %s" % (f_path, e)
        ) from e


def _read_from_json(f_path, is_stream=False):
    if is_stream:
        try:
            return json.loads(f_path)
        except ValueError as e:
            raise PolyaxonSchemaError("Json error: %s" % e) from e
    try:
        with open(f_path) as f:
            return json.loads(f.read())
    except ValueError as e:
        raise PolyaxonSchemaError(
            "Received non valid json: `%s`.\n" "Json error %s" % (f_path, e)
        ) from e
