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
from typing import Tuple


def get_component_full_name(component: str, owner: str = None, tag: str = None) -> str:
    if tag:
        component = "{}:{}".format(component, tag)
    if owner:
        component = "{}/{}".format(owner, component)

    return component


def get_component_info(component: str) -> Tuple[str, str, str]:
    parts = component.replace(".", "/").split("/")
    owner = "polyaxon"
    tag = None
    if len(parts) == 2:
        owner, component = parts
    parts = component.split(":")
    if len(parts) == 2:
        component, tag = parts
    return owner, component, tag
