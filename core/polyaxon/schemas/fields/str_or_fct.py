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

from marshmallow import fields


class StrOrFct(fields.Str):
    def serialize(self, attr, obj, accessor=None, **kwargs):
        value = getattr(obj, attr)
        if hasattr(value, "__call__") and hasattr(value, "__name__"):
            return value.__name__

        return super().serialize(attr, obj, accessor)
