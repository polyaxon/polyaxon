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

import numpy as np


def uniform(low, high, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.uniform(low=low, high=high, size=size)


def quniform(low, high, q, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def loguniform(low, high, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.exp(value)


def qloguniform(low, high, q, size=None, rand_generator=None):
    value = loguniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def normal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.normal(loc=loc, scale=scale, size=size)


def qnormal(loc, scale, q, size=None, rand_generator=None):
    draw = normal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q


def lognormal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.lognormal(mean=loc, sigma=scale, size=size)


def qlognormal(loc, scale, q, size=None, rand_generator=None):
    draw = lognormal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q
