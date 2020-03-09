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

from collections import Mapping

from marshmallow import ValidationError, fields

from polyaxon.schemas.utils import to_camel_case, to_snake_case


class SwaggerField(fields.Field):
    def __init__(self, cls, defaults=None, **kwargs):
        super().__init__(**kwargs)
        self.cls = cls
        self.defaults = defaults or {}

    def _get_object(self, value):
        try:
            for k in self.defaults:
                value[k] = value.get(k, self.defaults.get(k))
            return self.cls(**{to_snake_case(k): value[k] for k in value})
        except Exception as e:
            raise ValidationError(
                "Error initializing {}, {}".format(self.cls.__name__, e)
            )

    def _serialize(self, value, attr, obj, **kwargs):
        if not value:
            return value

        value = value.to_dict()
        keys = set(value.keys())
        for k in keys:
            if value[k] is None:
                del value[k]
        return {to_camel_case(k): value[k] for k in value}

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, Mapping):
            return self._get_object(value)

        if isinstance(value, self.cls):
            return value

        raise ValidationError(
            "This field expects a dict or an instance of {}.".format(self.cls.__name__)
        )
