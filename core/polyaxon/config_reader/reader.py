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

from collections import Mapping

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.config_reader.utils import deep_update
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.utils.list_utils import to_list


def read(config_values, config_type=None):
    """Reads an ordered list of configuration values and deep merge the values in reverse order."""
    if not config_values:
        raise PolyaxonSchemaError(
            "Cannot read config_value: `{}`".format(config_values)
        )

    config_values = to_list(config_values, check_none=True)

    config = {}
    for config_value in config_values:
        config_value = ConfigSpec.get_from(value=config_value, config_type=config_type)
        config_value.check_type()
        config_results = config_value.read()
        if config_results and isinstance(config_results, Mapping):
            config = deep_update(config, config_results)
        elif config_value.check_if_exists:
            raise PolyaxonSchemaError(
                "Cannot read config_value: `{}`".format(config_value)
            )

    return config
