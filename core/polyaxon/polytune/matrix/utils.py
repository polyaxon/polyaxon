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

import copy
import numpy as np

from marshmallow import ValidationError

from polyaxon.polyflow import (
    V1HpChoice,
    V1HpGeomSpace,
    V1HpLinSpace,
    V1HpLogNormal,
    V1HpLogSpace,
    V1HpLogUniform,
    V1HpNormal,
    V1HpPChoice,
    V1HpQLogNormal,
    V1HpQLogUniform,
    V1HpQNormal,
    V1HpQUniform,
    V1HpRange,
    V1HpUniform,
)
from polyaxon.polyflow.matrix.params import pchoice
from polyaxon.polytune.matrix import dist


def space_sample(value, size, rand_generator):
    size = None if size == 1 else size
    rand_generator = rand_generator or np.random
    try:
        return rand_generator.choice(value, size=size)
    except ValueError:
        idx = rand_generator.randint(0, len(value))
        return value[idx]


def dist_sample(fct, value, size, rand_generator):
    size = None if size == 1 else size
    rand_generator = rand_generator or np.random
    value = copy.deepcopy(value)
    value["size"] = size
    value["rand_generator"] = rand_generator
    return fct(**value)


def get_length(matrix):
    if matrix.IDENTIFIER == V1HpChoice.IDENTIFIER:
        return len(matrix.value)
    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        return len(matrix.value)

    if matrix.IDENTIFIER == V1HpRange.IDENTIFIER:
        return len(np.arange(**matrix.value))

    if matrix.IDENTIFIER == V1HpLinSpace.IDENTIFIER:
        return len(np.linspace(**matrix.value))

    if matrix.IDENTIFIER == V1HpLogSpace.IDENTIFIER:
        return len(np.logspace(**matrix.value))

    if matrix.IDENTIFIER == V1HpGeomSpace.IDENTIFIER:
        return len(np.geomspace(**matrix.value))

    if matrix.IDENTIFIER in {
        V1HpUniform.IDENTIFIER,
        V1HpQUniform.IDENTIFIER,
        V1HpLogUniform.IDENTIFIER,
        V1HpQLogUniform.IDENTIFIER,
        V1HpNormal.IDENTIFIER,
        V1HpQNormal.IDENTIFIER,
        V1HpLogNormal.IDENTIFIER,
        V1HpQLogNormal.IDENTIFIER,
    }:
        raise ValidationError("Distribution should not call `length`")


def get_min(matrix):
    if matrix.IDENTIFIER == V1HpChoice.IDENTIFIER:
        if matrix.is_categorical:
            return None
        return min(to_numpy(matrix))

    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        return None

    if matrix.IDENTIFIER in {
        V1HpRange.IDENTIFIER,
        V1HpLinSpace.IDENTIFIER,
        V1HpLogSpace.IDENTIFIER,
        V1HpGeomSpace.IDENTIFIER,
    }:
        return matrix.value.get("start")

    if matrix.IDENTIFIER == V1HpUniform.IDENTIFIER:
        return matrix.value.get("low")

    if matrix.IDENTIFIER in {
        V1HpQUniform.IDENTIFIER,
        V1HpLogUniform.IDENTIFIER,
        V1HpQLogUniform.IDENTIFIER,
        V1HpNormal.IDENTIFIER,
        V1HpQNormal.IDENTIFIER,
        V1HpLogNormal.IDENTIFIER,
        V1HpQLogNormal.IDENTIFIER,
    }:
        return None


def get_max(matrix):
    if matrix.IDENTIFIER == V1HpChoice.IDENTIFIER:
        if matrix.is_categorical:
            return None
        return max(to_numpy(matrix))

    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        return None

    if matrix.IDENTIFIER in {
        V1HpRange.IDENTIFIER,
        V1HpLinSpace.IDENTIFIER,
        V1HpLogSpace.IDENTIFIER,
        V1HpGeomSpace.IDENTIFIER,
    }:
        return matrix.value.get("stop")

    if matrix.IDENTIFIER == V1HpUniform.IDENTIFIER:
        return matrix.value.get("high")

    if matrix.IDENTIFIER in {
        V1HpQUniform.IDENTIFIER,
        V1HpLogUniform.IDENTIFIER,
        V1HpQLogUniform.IDENTIFIER,
        V1HpNormal.IDENTIFIER,
        V1HpQNormal.IDENTIFIER,
        V1HpLogNormal.IDENTIFIER,
        V1HpQLogNormal.IDENTIFIER,
    }:
        return None


def to_numpy(matrix):
    if matrix.IDENTIFIER == V1HpChoice.IDENTIFIER:
        return matrix.value
    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        raise ValidationError(
            "Distribution should not call `to_numpy`, "
            "instead it should call `sample`."
        )

    if matrix.IDENTIFIER == V1HpRange.IDENTIFIER:
        return np.arange(**matrix.value)

    if matrix.IDENTIFIER == V1HpLinSpace.IDENTIFIER:
        return np.linspace(**matrix.value)

    if matrix.IDENTIFIER == V1HpLogSpace.IDENTIFIER:
        return np.logspace(**matrix.value)

    if matrix.IDENTIFIER == V1HpGeomSpace.IDENTIFIER:
        return np.geomspace(**matrix.value)

    if matrix.IDENTIFIER in {
        V1HpUniform.IDENTIFIER,
        V1HpQUniform.IDENTIFIER,
        V1HpLogUniform.IDENTIFIER,
        V1HpQLogUniform.IDENTIFIER,
        V1HpNormal.IDENTIFIER,
        V1HpQNormal.IDENTIFIER,
        V1HpLogNormal.IDENTIFIER,
        V1HpQLogNormal.IDENTIFIER,
    }:
        raise ValidationError(
            "Distribution should not call `to_numpy`, "
            "instead it should call `sample`."
        )


def sample(matrix, size=None, rand_generator=None):
    size = None if size == 1 else size

    if matrix.IDENTIFIER == V1HpChoice.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )
    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        return pchoice(values=matrix.value, size=size, rand_generator=rand_generator)

    if matrix.IDENTIFIER == V1HpRange.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == V1HpLinSpace.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == V1HpLogSpace.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == V1HpGeomSpace.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == V1HpUniform.IDENTIFIER:
        return dist_sample(dist.uniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpQUniform.IDENTIFIER:
        return dist_sample(dist.quniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpLogUniform.IDENTIFIER:
        return dist_sample(dist.loguniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpQLogUniform.IDENTIFIER:
        return dist_sample(dist.qloguniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpNormal.IDENTIFIER:
        return dist_sample(dist.normal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpQNormal.IDENTIFIER:
        return dist_sample(dist.qnormal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpLogNormal.IDENTIFIER:
        return dist_sample(dist.lognormal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == V1HpQLogNormal.IDENTIFIER:
        return dist_sample(dist.qlognormal, matrix.value, size, rand_generator)
