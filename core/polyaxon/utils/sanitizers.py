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

from collections.abc import Mapping
from typing import Dict


def sanitize_value(d, handle_dict: bool = False):
    if isinstance(d, str):
        return d
    if not isinstance(d, Mapping):
        return json.dumps(d)
    if not handle_dict:
        return json.dumps(d)
    return {d_k: sanitize_value(d_v, handle_dict=True) for d_k, d_v in d.items()}


def sanitize_string_dict(d: Dict[str, str] = None):
    if isinstance(d, Mapping):
        return {d_k: sanitize_value(d_v, handle_dict=False) for d_k, d_v in d.items()}
    return d
