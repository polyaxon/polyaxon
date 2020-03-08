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

from marshmallow import ValidationError, fields


class Tensor(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            return [value, 0, 0]
        if isinstance(value, list) and len(value) == 3:
            condition = (
                isinstance(value[0], str)
                and isinstance(value[1], int)
                and isinstance(value[1], int)
            )
            if condition:
                return value
        raise ValidationError("This field expects a str or a list of [str, int, int].")
