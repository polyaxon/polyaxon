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

try:
    import numpy as np
except ImportError:
    np = None


def to_list(value, check_none=False, check_dict=False):
    if check_none and value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    if np and isinstance(value, np.ndarray):
        return value.tolist()
    if check_dict and isinstance(value, Mapping):
        return list(value.items())
    return [value]
