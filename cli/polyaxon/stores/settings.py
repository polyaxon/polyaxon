#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
import os

from polyaxon.config_reader.manager import ConfigManager

config = ConfigManager.read_configs([os.environ])


RUN_STORES_ACCESS_KEYS = config.get_dict(
    "POLYSTORES_RUN_STORES_ACCESS_KEYS", is_optional=True, default={}
)
TMP_AUTH_GCS_ACCESS_PATH = config.get_string(
    "POLYSTORES_TMP_AUTH_GCS_ACCESS_PATH",
    is_optional=True,
    default="/tmp/.polyaxon/.gcsaccess.json",
)
