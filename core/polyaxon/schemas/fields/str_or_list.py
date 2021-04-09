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

from marshmallow import fields


class StrOrList(fields.Str):
    default_error_messages = {
        "invalid": "Not a valid string or list.",
        "invalid_utf8": "Not a valid utf-8 string.",
    }

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, (list, tuple)):
            return value

        return super()._serialize(value=value, attr=attr, obj=obj)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (list, tuple)):
            return value

        return super()._deserialize(value=value, attr=attr, data=data)
