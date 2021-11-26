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

import jinja2

from markupsafe import soft_str


def map_format(value, pattern, variable_name: str = None):
    if variable_name:
        return soft_str(pattern) % {variable_name: value}
    return soft_str(pattern) % value


def get_engine():
    env = jinja2.Environment()
    env.filters["map_format"] = map_format
    return env
