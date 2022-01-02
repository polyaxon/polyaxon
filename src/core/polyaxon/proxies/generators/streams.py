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
from polyaxon.proxies.generators.base import write_to_conf_file
from polyaxon.proxies.schemas.streams import get_base_config, get_main_config


def generate_streams_conf(path=None, root=None):
    write_to_conf_file("polyaxon.main", get_main_config(root), path)
    write_to_conf_file("polyaxon.base", get_base_config(), path)
