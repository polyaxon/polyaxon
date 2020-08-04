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

from collections.abc import Mapping


def deep_update(config, override_config):
    for k, v in override_config.items():
        if isinstance(v, Mapping):
            k_config = config.get(k, {})
            if isinstance(k_config, Mapping):
                v_config = deep_update(k_config, v)
                config[k] = v_config
            else:
                config[k] = v
        else:
            config[k] = override_config[k]
    return config
