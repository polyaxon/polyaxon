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
import logging

from collections.abc import Mapping

try:
    import numpy as np
except ImportError:
    np = None


def to_list(value, check_none=False, check_dict=False, to_unique: bool = False):
    def _to_unique(v):
        try:
            return list(dict.fromkeys(v))
        except Exception as e:
            logging.debug("Could not return unique value for list. Error %s", e)
            return list(v)

    if check_none and value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return _to_unique(value) if to_unique else list(value)
    if np and isinstance(value, np.ndarray):
        value = value.tolist()
        return _to_unique(value) if to_unique else value
    if check_dict and isinstance(value, Mapping):
        return list(value.items())
    return [value]
