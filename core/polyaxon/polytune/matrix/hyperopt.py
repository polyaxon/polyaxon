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

import hyperopt

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
from polyaxon.polytune.matrix.utils import to_numpy


def to_hyperopt(name, matrix):
    if matrix.IDENTIFIER in {
        V1HpChoice.IDENTIFIER,
        V1HpRange.IDENTIFIER,
        V1HpLinSpace.IDENTIFIER,
        V1HpLogSpace.IDENTIFIER,
        V1HpGeomSpace.IDENTIFIER,
    }:
        return hyperopt.hp.choice(name, to_numpy(matrix))

    if matrix.IDENTIFIER == V1HpPChoice.IDENTIFIER:
        raise ValidationError(
            "{} is not supported by Hyperopt.".format(matrix.IDENTIFIER)
        )

    if matrix.IDENTIFIER == V1HpUniform.IDENTIFIER:
        return hyperopt.hp.uniform(
            name, matrix.value.get("low"), matrix.value.get("high")
        )

    if matrix.IDENTIFIER == V1HpQUniform.IDENTIFIER:
        return hyperopt.hp.quniform(
            name,
            matrix.value.get("low"),
            matrix.value.get("high"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == V1HpLogUniform.IDENTIFIER:
        return hyperopt.hp.loguniform(
            name, matrix.value.get("low"), matrix.value.get("high")
        )

    if matrix.IDENTIFIER == V1HpQLogUniform.IDENTIFIER:
        return hyperopt.hp.qloguniform(
            name,
            matrix.value.get("low"),
            matrix.value.get("high"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == V1HpNormal.IDENTIFIER:
        return hyperopt.hp.normal(
            name, matrix.value.get("loc"), matrix.value.get("scale")
        )

    if matrix.IDENTIFIER == V1HpQNormal.IDENTIFIER:
        return hyperopt.hp.qnormal(
            name,
            matrix.value.get("loc"),
            matrix.value.get("scale"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == V1HpLogNormal.IDENTIFIER:
        return hyperopt.hp.lognormal(
            name, matrix.value.get("loc"), matrix.value.get("scale")
        )

    if matrix.IDENTIFIER == V1HpQLogNormal.IDENTIFIER:
        return hyperopt.hp.qlognormal(
            name,
            matrix.value.get("loc"),
            matrix.value.get("scale"),
            matrix.value.get("q"),
        )
