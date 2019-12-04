#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import ast
import copy
import six

from collections import Mapping

from marshmallow import fields, validate, validates_schema
from marshmallow.exceptions import ValidationError

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema

try:
    import numpy as np
except (ImportError, ModuleNotFoundError):
    np = None


# pylint:disable=redefined-outer-name


class PChoice(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            if isinstance(value[1], float) and 0 <= value[1] < 1:
                return value
        raise ValidationError("This field expects a list of [value<Any>, dist<float>].")


class Range(fields.Field):
    REQUIRED_KEYS = ["start", "stop", "step"]
    OPTIONAL_KEY = None
    KEYS = REQUIRED_KEYS
    CHECK_ORDER = True

    def _deserialize(
        self, value, attr, data, **kwargs
    ):  # pylint:disable=too-many-branches
        if isinstance(value, six.string_types):
            value = value.split(":")
        elif isinstance(value, Mapping):
            if set(self.REQUIRED_KEYS) - set(six.iterkeys(value)):
                raise ValidationError(
                    "{} dict must have {} keys {}.".format(
                        self.__class__.__name__,
                        len(self.REQUIRED_KEYS),
                        self.REQUIRED_KEYS,
                    )
                )
            if len(value) == len(self.REQUIRED_KEYS):
                value = [value[k] for k in self.REQUIRED_KEYS]
            elif len(value) == len(self.KEYS):
                value = [value[k] for k in self.KEYS]
        elif not isinstance(value, list):
            raise ValidationError(
                "{} accept values formatted as the following:\n"
                " * str: {}\n"
                " * dict: {}\n"
                " * list: {}".format(
                    self.__class__.__name__,
                    ":".join(self.REQUIRED_KEYS),
                    dict(
                        zip(
                            self.REQUIRED_KEYS,
                            ["v{}".format(i) for i in range(len(self.REQUIRED_KEYS))],
                        )
                    ),
                    self.REQUIRED_KEYS,
                )
            )

        if len(value) != len(self.REQUIRED_KEYS) and len(value) != len(self.KEYS):
            raise ValidationError(
                "{} requires {} or {} elements received {}".format(
                    self.__class__.__name__,
                    len(self.REQUIRED_KEYS),
                    len(self.KEYS),
                    len(value),
                )
            )

        for i, v in enumerate(value):
            try:
                float(v)
            except (ValueError, TypeError):
                raise ValidationError(
                    "{}: {} must of type int or float, received instead {}".format(
                        self.__class__.__name__, self.REQUIRED_KEYS[i], v
                    )
                )
            if not isinstance(v, (int, float)):
                value[i] = ast.literal_eval(v)

        # Check that lower value is smaller than higher value
        if self.CHECK_ORDER and value[0] >= value[1]:
            raise ValidationError(
                "{key2} value must be strictly higher that {key1} value, "
                "received instead {key1}: {val1}, {key2}: {val2}".format(
                    key1=self.REQUIRED_KEYS[0],
                    key2=self.REQUIRED_KEYS[1],
                    val1=value[0],
                    val2=value[1],
                )
            )
        if len(self.REQUIRED_KEYS) == 3 and value[2] == 0:
            raise ValidationError("{} cannot be 0".format(self.REQUIRED_KEYS[2]))

        value = dict(zip(self.KEYS, value))
        return value


class LinSpace(Range):
    REQUIRED_KEYS = ["start", "stop", "num"]
    KEYS = REQUIRED_KEYS


class GeomSpace(Range):
    REQUIRED_KEYS = ["start", "stop", "num"]
    KEYS = REQUIRED_KEYS


class LogSpace(Range):
    REQUIRED_KEYS = ["start", "stop", "num"]
    OPTIONAL_KEYS = ["base"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def validate_pchoice(values):
    dists = [v for v in values if v]
    if sum(dists) > 1:
        raise ValidationError("The distribution of different outcomes should sum to 1.")


def pchoice(values, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    keys = [v[0] for v in values]
    dists = [v[1] for v in values]
    validate_pchoice(dists)
    indices = rand_generator.multinomial(1, dists, size=size)
    if size is None:
        return keys[indices.argmax()]
    return [keys[ind.argmax()] for ind in indices]


class Dist(Range):
    CHECK_ORDER = False


class Uniform(Dist):
    REQUIRED_KEYS = ["low", "high"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QUniform(Dist):
    REQUIRED_KEYS = ["low", "high", "q"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogUniform(Dist):
    REQUIRED_KEYS = ["low", "high"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogUniform(Dist):
    REQUIRED_KEYS = ["low", "high", "q"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class Normal(Dist):
    REQUIRED_KEYS = ["loc", "scale"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QNormal(Dist):
    REQUIRED_KEYS = ["loc", "scale", "q"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogNormal(Dist):
    REQUIRED_KEYS = ["loc", "scale"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogNormal(Dist):
    REQUIRED_KEYS = ["loc", "scale", "q"]
    OPTIONAL_KEYS = ["size"]
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def validate_matrix(values):
    v = sum(map(lambda x: 1 if x else 0, values))
    if v == 0 or v > 1:
        raise ValidationError(
            "Matrix element is not valid, one and only one option is required."
        )


class MatrixChoiceSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("choice"))
    value = fields.List(fields.Raw(), allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixChoiceConfig


class MatrixChoiceConfig(BaseConfig):
    SCHEMA = MatrixChoiceSchema
    IDENTIFIER = "choice"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return False

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return any(
            [
                v
                for v in self.value
                if not isinstance(v, (int, float, complex, np.integer, np.floating))
            ]
        )

    @property
    def is_uniform(self):
        return False


class MatrixPChoiceSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("pchoice"))
    value = fields.List(PChoice(), allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixPChoiceConfig

    @validates_schema
    def validate_pchoice(self, data):
        if data.get("value"):
            validate_pchoice(values=[v[1] for v in data["value"] if v])


class MatrixPChoiceConfig(BaseConfig):
    SCHEMA = MatrixPChoiceSchema
    IDENTIFIER = "pchoice"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

        if value:
            validate_pchoice(values=[v[1] for v in value if v])

    @property
    def is_distribution(self):
        return True

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False

    @property
    def is_uniform(self):
        return False


class MatrixRangeSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("range"))
    value = Range(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixRangeConfig


class MatrixRangeConfig(BaseConfig):
    SCHEMA = MatrixRangeSchema
    IDENTIFIER = "range"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return False

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return True

    @property
    def is_categorical(self):
        return False

    @property
    def is_uniform(self):
        return False


class MatrixLinSpaceSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("linspace"))
    value = LinSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixLinSpaceConfig


class MatrixLinSpaceConfig(BaseConfig):
    SCHEMA = MatrixLinSpaceSchema
    IDENTIFIER = "linspace"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return False

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return True

    @property
    def is_categorical(self):
        return False

    @property
    def is_uniform(self):
        return False


class MatrixLogSpaceSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("logspace"))
    value = LogSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixLogSpaceConfig


class MatrixLogSpaceConfig(BaseConfig):
    SCHEMA = MatrixLogSpaceSchema
    IDENTIFIER = "logspace"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return False

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return True

    @property
    def is_categorical(self):
        return False

    @property
    def is_uniform(self):
        return False


class MatrixGeomSpaceSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("geomspace"))
    value = GeomSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixGeomSpaceConfig


class MatrixGeomSpaceConfig(BaseConfig):
    SCHEMA = MatrixGeomSpaceSchema
    IDENTIFIER = "geomspace"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return False

    @property
    def is_continuous(self):
        return False

    @property
    def is_discrete(self):
        return True

    @property
    def is_range(self):
        return True

    @property
    def is_categorical(self):
        return False

    @property
    def is_uniform(self):
        return False


class MatrixUniformSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("uniform"))
    value = Uniform(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixUniformConfig


class MatrixUniformConfig(BaseConfig):
    SCHEMA = MatrixUniformSchema
    IDENTIFIER = "uniform"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return True

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixQUniformSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("quniform"))
    value = QUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixQUniformConfig


class MatrixQUniformConfig(BaseConfig):
    SCHEMA = MatrixQUniformSchema
    IDENTIFIER = "quniform"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixLogUniformSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("loguniform"))
    value = LogUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixLogUniformConfig


class MatrixLogUniformConfig(BaseConfig):
    SCHEMA = MatrixLogUniformSchema
    IDENTIFIER = "loguniform"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixQLogUniformSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qloguniform"))
    value = QLogUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixQLogUniformConfig


class MatrixQLogUniformConfig(BaseConfig):
    SCHEMA = MatrixQLogUniformSchema
    IDENTIFIER = "qloguniform"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False

    @property
    def min(self):
        return None


class MatrixNormalSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("normal"))
    value = Normal(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixNormalConfig


class MatrixNormalConfig(BaseConfig):
    SCHEMA = MatrixNormalSchema
    IDENTIFIER = "normal"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixQNormalSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qnormal"))
    value = QNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixQNormalConfig


class MatrixQNormalConfig(BaseConfig):
    SCHEMA = MatrixQNormalSchema
    IDENTIFIER = "qnormal"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixLogNormalSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("lognormal"))
    value = LogNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixLogNormalConfig


class MatrixLogNormalConfig(BaseConfig):
    SCHEMA = MatrixLogNormalSchema
    IDENTIFIER = "lognormal"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixQLogNormalSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qlognormal"))
    value = QLogNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixQLogNormalConfig


class MatrixQLogNormalConfig(BaseConfig):
    SCHEMA = MatrixQLogNormalSchema
    IDENTIFIER = "qlognormal"

    def __init__(self, value, kind=IDENTIFIER):
        self.kind = kind
        self.value = value

    @property
    def is_distribution(self):
        return True

    @property
    def is_uniform(self):
        return False

    @property
    def is_continuous(self):
        return True

    @property
    def is_discrete(self):
        return False

    @property
    def is_range(self):
        return False

    @property
    def is_categorical(self):
        return False


class MatrixSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MatrixChoiceConfig.IDENTIFIER: MatrixChoiceSchema,
        MatrixPChoiceConfig.IDENTIFIER: MatrixPChoiceSchema,
        MatrixRangeConfig.IDENTIFIER: MatrixRangeSchema,
        MatrixLinSpaceConfig.IDENTIFIER: MatrixLinSpaceSchema,
        MatrixLogSpaceConfig.IDENTIFIER: MatrixLogSpaceSchema,
        MatrixGeomSpaceConfig.IDENTIFIER: MatrixGeomSpaceSchema,
        MatrixUniformConfig.IDENTIFIER: MatrixUniformSchema,
        MatrixQUniformConfig.IDENTIFIER: MatrixQUniformSchema,
        MatrixLogUniformConfig.IDENTIFIER: MatrixLogUniformSchema,
        MatrixQLogUniformConfig.IDENTIFIER: MatrixQLogUniformSchema,
        MatrixNormalConfig.IDENTIFIER: MatrixNormalSchema,
        MatrixQNormalConfig.IDENTIFIER: MatrixQNormalSchema,
        MatrixLogNormalConfig.IDENTIFIER: MatrixLogNormalSchema,
        MatrixQLogNormalConfig.IDENTIFIER: MatrixQLogNormalSchema,
    }
