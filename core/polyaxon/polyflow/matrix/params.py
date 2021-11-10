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

import ast

from collections.abc import Mapping
from typing import Any, Union

import polyaxon_sdk

from marshmallow import fields, validate, validates_schema
from marshmallow.exceptions import ValidationError

from polyaxon import types
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig, BaseOneOfSchema
from polyaxon.utils.serialization import (
    date_deserialize,
    date_serialize,
    datetime_deserialize,
    datetime_serialize,
    timedelta_deserialize,
    timedelta_serialize,
)
from polyaxon.utils.signal_decorators import check_partial

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
    ACCEPT_STR_VALUE = True

    def _validate_value(self, value, attr, data, **kwargs):
        if self.ACCEPT_STR_VALUE and isinstance(value, str):
            value = value.split(":")
        elif isinstance(value, Mapping):
            if set(self.REQUIRED_KEYS) - set(value.keys()):
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
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        value = self._validate_value(value, attr, data, **kwargs)

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


class DateRange(Range):
    REQUIRED_KEYS = ["start", "stop", "step"]
    KEYS = REQUIRED_KEYS
    ACCEPT_STR_VALUE = False

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        return {
            "start": date_serialize("start", value),
            "stop": date_serialize("stop", value),
            "step": value["step"],
        }

    def _deserialize(self, value, attr, data, **kwargs):
        value = self._validate_value(value, attr, data, **kwargs)

        def _date_deserialize(i, v):
            try:
                return date_deserialize(v)
            except Exception as e:
                raise ValidationError(
                    "{}: {} must of type date, received instead {}. Error {}".format(
                        self.__class__.__name__, self.REQUIRED_KEYS[i], v, e
                    )
                )

        try:
            frequency = int(value[2])
        except Exception as e:
            raise ValidationError(
                "{}: {} must of type int, received instead {}. Error {}".format(
                    self.__class__.__name__, self.REQUIRED_KEYS[2], value[2], e
                )
            )

        value = [
            _date_deserialize(0, value[0]),
            _date_deserialize(1, value[1]),
            frequency,
        ]

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


class DateTimeRange(Range):
    REQUIRED_KEYS = ["start", "stop", "step"]
    KEYS = REQUIRED_KEYS
    ACCEPT_STR_VALUE = False

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        return {
            "start": datetime_serialize("start", value),
            "stop": datetime_serialize("stop", value),
            "step": timedelta_serialize("step", value),
        }

    def _deserialize(self, value, attr, data, **kwargs):
        value = self._validate_value(value, attr, data, **kwargs)

        def _datetime_deserialize(i, v):
            try:
                return datetime_deserialize(v)
            except Exception as e:
                raise ValidationError(
                    "{}: {} must of type datetime, received instead {}. Error {}".format(
                        self.__class__.__name__, self.REQUIRED_KEYS[i], v, e
                    )
                )

        try:
            frequency = timedelta_deserialize(value[2])
        except Exception as e:
            raise ValidationError(
                "{}: {} must of type int(timedelta), received instead {}. Error {}".format(
                    self.__class__.__name__, self.REQUIRED_KEYS[2], value[2], e
                )
            )

        value = [
            _datetime_deserialize(0, value[0]),
            _datetime_deserialize(1, value[1]),
            frequency,
        ]

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


class BaseHpParamConfig(BaseConfig):
    @staticmethod
    def validate_io(io: "V1IO"):  # noqa
        if io.type not in [types.INT, types.FLOAT]:
            raise ValidationError(
                "Param `{}` has a an input type `{}` "
                "and it does not correspond to hyper-param type `int or float`.".format(
                    io.name,
                    io.type,
                )
            )
        return True


class HpChoiceSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("choice"))
    value = fields.List(fields.Raw(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpChoice


class V1HpChoice(BaseHpParamConfig, polyaxon_sdk.V1HpChoice):
    """`Choice` picks a value from a of list values.

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: choice
    >>>     value: [1, 2, 3, 4, 5]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpChoice
    >>> param_test = V1HpChoice(value=[1, 2, 3, 4, 5])
    ```
    """

    SCHEMA = HpChoiceSchema
    IDENTIFIER = "choice"

    @staticmethod
    def validate_io(io: "V1IO"):  # noqa
        return True

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


class HpPChoiceSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("pchoice"))
    value = fields.List(PChoice(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpPChoice

    @validates_schema
    @check_partial
    def validate_pchoice(self, data, **kwargs):
        if data.get("value"):
            validate_pchoice(values=[v[1] for v in data["value"] if v])


class V1HpPChoice(BaseHpParamConfig, polyaxon_sdk.V1HpPChoice):
    """`PChoice` picks a value with a probability from a list of
    [(value, probability), (value, probability), ...].

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: pchoice
    >>>     value: [(1, 0.1), (2, 0.1), (3, 0.8)]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpPChoice
    >>> param_test = V1HpPChoice(value=[("A", 0.1), ("B", 0.1), ("C", 0.8)])
    ```
    """

    SCHEMA = HpPChoiceSchema
    IDENTIFIER = "pchoice"

    @staticmethod
    def validate_io(io: "V1IO"):  # noqa
        return True

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


class HpRangeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("range"))
    value = Range(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpRange


class V1HpRange(BaseHpParamConfig, polyaxon_sdk.V1HpRange):
    """`Range` picks a value from a generated list of values using `[start, stop, step]`,
    you can pass values in these forms:
      * [1, 10, 2]
      * {start: 1, stop: 10, step: 2}
      * '1:10:2'

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: range
    >>>     value: [1, 10, 2]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpRange
    >>> param_test = V1HpRange(value=[1, 10, 2])
    ```
    """

    SCHEMA = HpRangeSchema
    IDENTIFIER = "range"

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


class HpDateRangeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("daterange"))
    value = DateRange(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpDateRange


class V1HpDateRange(BaseHpParamConfig, polyaxon_sdk.V1HpDateRange):
    """`DateRange` picks a value from a generated list of values using `[start, stop, step]`,
    you can pass values in these forms:
      * `["2019-06-24", "2019-06-25", 3600 * 24]`
      * `{start: "2019-06-24 00:00", stop: "2019-06-28 00:00", step: 1}`

    **Step (frequency)**: represents a timedelta in days.

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: daterange
    >>>     value: ["2019-06-22", "2019-07-25", 1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpDateRange
    >>> param_test = V1HpDateRange(value=["2019-06-22", "2019-06-25", 2])
    ```
    """

    SCHEMA = HpDateRangeSchema
    IDENTIFIER = "daterange"

    @staticmethod
    def validate_io(io: "V1IO"):  # noqa
        if io.type != types.DATE:
            raise ValidationError(
                "Param `{}` has a an input type `{}` "
                "and it does not correspond to hyper-param type `date`.".format(
                    io.name,
                    io.type,
                )
            )
        return True

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


class HpDateTimeRangeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("datetimerange"))
    value = DateTimeRange(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpDateTimeRange


class V1HpDateTimeRange(BaseHpParamConfig, polyaxon_sdk.V1HpDateTimeRange):
    """`DateTimeRange` picks a value from a generated list of values using `[start, stop, step]`,
    you can pass values in these forms:
      * `["2019-06-24T21:20:07+02:00", "2019-06-25T21:20:07+02:00", 3600]`
      * `{start: "2019-06-24 00:00", stop: "2019-06-28 00:00", step: 3600 * 4}`

    **Step (frequency)**: represents a timedelta in seconds.

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: datetimerange
    >>>     value: ["2019-06-22 21:00", "2019-06-25 21:00", 3600]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpDateTimeRange
    >>> param_test = V1HpDateTimeRange(value=["2019-06-22 21:00", "2019-06-25 21:00", 3600])
    ```
    """

    SCHEMA = HpDateTimeRangeSchema
    IDENTIFIER = "datetimerange"

    @staticmethod
    def validate_io(io: "V1IO"):  # noqa
        if io.type != types.DATETIME:
            raise ValidationError(
                "Param `{}` has a an input type `{}` "
                "and it does not correspond to hyper-param type `datetime`.".format(
                    io.name,
                    io.type,
                )
            )
        return True

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


class HpLinSpaceSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("linspace"))
    value = LinSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpLinSpace


class V1HpLinSpace(BaseHpParamConfig, polyaxon_sdk.V1HpLinSpace):
    """`LinSpace` picks a value from a generated list of steps from start to stop spaced evenly
    on a linear scale `[start, stop, step]`, you can pass values in these forms:
      * [1, 10, 20]
      * {start: 1, stop: 10, num: 20}
      * '1:10:20'

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: linspace
    >>>     value: [1, 10, 20]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpLinSpace
    >>> param_test = V1HpLinSpace(value=[1, 10, 20])
    ```
    """

    SCHEMA = HpLinSpaceSchema
    IDENTIFIER = "linspace"

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


class HpLogSpaceSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("logspace"))
    value = LogSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpLogSpace


class V1HpLogSpace(BaseHpParamConfig, polyaxon_sdk.V1HpLogSpace):
    """`LogSpace` picks a value from a generated list of steps from start to stop spaced evenly
    on a log scale `[start, stop, step]`, you can pass values in these forms:
      * [1, 10, 20]
      * {start: 1, stop: 10, num: 20}
      * '1:10:20'

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: logspace
    >>>     value: [1, 10, 20]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpLogSpace
    >>> param_test = V1HpLinSpace(value=[1, 10, 20])
    ```
    """

    SCHEMA = HpLogSpaceSchema
    IDENTIFIER = "logspace"

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


class HpGeomSpaceSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("geomspace"))
    value = GeomSpace(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpGeomSpace


class V1HpGeomSpace(BaseHpParamConfig, polyaxon_sdk.V1HpGeomSpace):
    """`GeomSpace` picks a value from a generated list of steps from start to stop spaced evenly
    on a geometric progression `[start, stop, step]`, you can pass values in these forms:
      * [1, 10, 20]
      * {start: 1, stop: 10, num: 20}
      * '1:10:20'

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: geomspace
    >>>     value: [1, 10, 20]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpGeomSpace
    >>> param_test = V1HpGeomSpace(value=[1, 10, 20])
    ```
    """

    SCHEMA = HpGeomSpaceSchema
    IDENTIFIER = "geomspace"

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


class HpUniformSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("uniform"))
    value = Uniform(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpUniform


class V1HpUniform(BaseHpParamConfig, polyaxon_sdk.V1HpUniform):
    """`Uniform` draws samples from a uniform distribution over the half-open
    interval `[low, high)`, you can pass values in these forms:
      * 0:1
      * [0, 1]
      * {'low': 0, 'high': 1}

    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: uniform
    >>>     value: [0, 1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpUniform
    >>> param_test = V1HpUniform(value=[0, 1])
    ```
    """

    SCHEMA = HpUniformSchema
    IDENTIFIER = "uniform"

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


class HpQUniformSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("quniform"))
    value = QUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpQUniform


class V1HpQUniform(BaseHpParamConfig, polyaxon_sdk.V1HpQUniform):
    """`QUniform` samples from a quantized uniform distribution over `[low, high]`
    (`round(uniform(low, high) / q) * q`),
    you can pass values in these forms:
      * 0:1:0.1
      * [0, 1, 0.1]
      * {'low': 0, 'high': 1, 'q': 0.1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: quniform
    >>>     value: [0, 1, 0.1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpQUniform
    >>> param_test = V1HpQUniform(value=[0, 1, 0.1])
    ```
    """

    SCHEMA = HpQUniformSchema
    IDENTIFIER = "quniform"

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


class HpLogUniformSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("loguniform"))
    value = LogUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpLogUniform


class V1HpLogUniform(BaseHpParamConfig, polyaxon_sdk.V1HpLogUniform):
    """`LogUniform` samples from a log uniform distribution over`[low, high]`,
    you can pass values in these forms:
      * 0:1
      * [0, 1]
      * {'low': 0, 'high': 1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: loguniform
    >>>     value: [0, 1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpLogUniform
    >>> param_test = V1HpLogUniform(value=[0, 1])
    ```
    """

    SCHEMA = HpLogUniformSchema
    IDENTIFIER = "loguniform"

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


class HpQLogUniformSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qloguniform"))
    value = QLogUniform(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpQLogUniform


class V1HpQLogUniform(BaseHpParamConfig, polyaxon_sdk.V1HpQLogUniform):
    """`LogUniform` samples from a log uniform distribution over`[low, high]`,
    you can pass values in these forms:
      * 0:1:0.1
      * [0, 1, 0.1]
      * {'low': 0, 'high': 1, 'q': 0.1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: qloguniform
    >>>     value: [0, 1, 0.1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpQLogUniform
    >>> param_test = V1HpQLogUniform(value=[0, 1, 0.1])
    ```
    """

    SCHEMA = HpQLogUniformSchema
    IDENTIFIER = "qloguniform"

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


class HpNormalSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("normal"))
    value = Normal(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpNormal


class V1HpNormal(BaseHpParamConfig, polyaxon_sdk.V1HpNormal):
    """`Normal` draws random samples from a normal (Gaussian) distribution defined by
    `[loc, scale]`, you can pass values in these forms:
      * 0:1
      * [0, 1]
      * {'loc': 0, 'scale': 1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: normal
    >>>     value: [0, 1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpNormal
    >>> param_test = V1HpNormal(value=[0, 1])
    ```
    """

    SCHEMA = HpNormalSchema
    IDENTIFIER = "normal"

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


class HpQNormalSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qnormal"))
    value = QNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpQNormal


class V1HpQNormal(BaseHpParamConfig, polyaxon_sdk.V1HpQNormal):
    """`QNormal` draws random samples from a quantized normal (Gaussian) distribution defined by
    `[loc, scale]`, you can pass values in these forms:
      * 0:1:0.1
      * [0, 1, 0.1]
      * {'loc': 0, 'scale': 1, 'q': 0.1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: qnormal
    >>>     value: [0, 1, 0.1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpQNormal
    >>> param_test = V1HpNormal(value=[0, 1, 0.1])
    ```
    """

    SCHEMA = HpQNormalSchema
    IDENTIFIER = "qnormal"

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


class HpLogNormalSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("lognormal"))
    value = LogNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpLogNormal


class V1HpLogNormal(BaseHpParamConfig, polyaxon_sdk.V1HpLogNormal):
    """`LogNormal` draws random samples from a log normal (Gaussian) distribution defined by
    `[loc, scale]`, you can pass values in these forms:
      * 0:1
      * [0, 1]
      * {'loc': 0, 'scale': 1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: lognormal
    >>>     value: [0, 1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpLogNormal
    >>> param_test = V1HpLogNormal(value=[0, 1])
    ```
    """

    SCHEMA = HpLogNormalSchema
    IDENTIFIER = "lognormal"

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


class HpQLogNormalSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("qlognormal"))
    value = QLogNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return V1HpQLogNormal


class V1HpQLogNormal(BaseHpParamConfig, polyaxon_sdk.V1HpQLogNormal):
    """`QLogNormal` draws random samples from a log normal (Gaussian) distribution defined by
    `[loc, scale]`, you can pass values in these forms:
      * 0:1:0.1
      * [0, 1, 0.1]
      * {'loc': 0, 'scale': 1, 'q': 0.1}


    ```yaml
    >>> params:
    >>>   paramTest:
    >>>     kind: qlognormal
    >>>     value: [0, 1, 0.1]
    ```

    ```python
    >>> from polyaxon.polyflow import V1HpQLogNormal
    >>> param_test = V1HpQLogNormal(value=[0, 1])
    ```
    """

    SCHEMA = HpQLogNormalSchema
    IDENTIFIER = "qlognormal"

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


class HpParamSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1HpChoice.IDENTIFIER: HpChoiceSchema,
        V1HpPChoice.IDENTIFIER: HpPChoiceSchema,
        V1HpRange.IDENTIFIER: HpRangeSchema,
        V1HpDateRange.IDENTIFIER: HpDateRangeSchema,
        V1HpDateTimeRange.IDENTIFIER: HpDateTimeRangeSchema,
        V1HpLinSpace.IDENTIFIER: HpLinSpaceSchema,
        V1HpLogSpace.IDENTIFIER: HpLogSpaceSchema,
        V1HpGeomSpace.IDENTIFIER: HpGeomSpaceSchema,
        V1HpUniform.IDENTIFIER: HpUniformSchema,
        V1HpQUniform.IDENTIFIER: HpQUniformSchema,
        V1HpLogUniform.IDENTIFIER: HpLogUniformSchema,
        V1HpQLogUniform.IDENTIFIER: HpQLogUniformSchema,
        V1HpNormal.IDENTIFIER: HpNormalSchema,
        V1HpQNormal.IDENTIFIER: HpQNormalSchema,
        V1HpLogNormal.IDENTIFIER: HpLogNormalSchema,
        V1HpQLogNormal.IDENTIFIER: HpQLogNormalSchema,
    }


V1HpParam = Union[
    V1HpChoice,
    V1HpPChoice,
    V1HpRange,
    V1HpDateRange,
    V1HpDateTimeRange,
    V1HpLinSpace,
    V1HpLogSpace,
    V1HpGeomSpace,
    V1HpUniform,
    V1HpQUniform,
    V1HpLogUniform,
    V1HpQLogUniform,
    V1HpNormal,
    V1HpQNormal,
    V1HpLogNormal,
    V1HpQLogNormal,
]
