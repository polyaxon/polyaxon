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

import math

try:
    import numpy as np
except ImportError:
    np = None


def sanitize_np_types(value):
    if isinstance(value, str):
        return value
    if math.isnan(value) or math.isinf(value):
        return None
    if isinstance(value, (int, float, complex, type(None))):
        return value
    if np and np.isnan(value):
        return None
    if np and isinstance(value, np.integer):
        return int(value)
    if np and isinstance(value, np.floating):
        return float(value)
    return value


def to_np(value):
    if isinstance(value, np.ndarray):
        return value
    if np.isscalar(value):
        return np.array([value])


def calculate_scale_factor(tensor):
    converted = tensor.numpy() if not isinstance(tensor, np.ndarray) else tensor
    return 1 if converted.dtype == np.uint8 else 255
