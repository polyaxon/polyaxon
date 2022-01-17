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

import copy

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyflow import V1Environment


def validate(spec, data):
    """Validates the data and creates the config objects"""
    data = copy.deepcopy(data)
    validated_data = {}

    def validate_keys(section, config, section_data):
        extra_args = [
            key for key in section_data.keys() if key not in config.SCHEMA().fields
        ]
        if extra_args:
            raise PolyaxonfileError(
                "Extra arguments passed for `{}`: {}".format(section, extra_args)
            )

    def add_validated_section(section, config):
        if data.get(section):
            section_data = data[section]
            validate_keys(section=section, config=config, section_data=section_data)
            validated_data[section] = config.from_dict(section_data)

    add_validated_section(spec.ENVIRONMENT, V1Environment)

    return validated_data
