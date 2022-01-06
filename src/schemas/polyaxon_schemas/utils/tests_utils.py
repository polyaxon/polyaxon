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

import numpy as np

from collections.abc import Mapping


def assert_equal_dict(dict1, dict2):
    for k, v in dict1.items():
        if v is None:
            continue
        if isinstance(v, Mapping):
            assert_equal_dict(v, dict2[k])
        else:
            assert v == dict2[k]


def tensor_np(shape, dtype=float):
    return np.arange(np.prod(shape), dtype=dtype).reshape(shape)
