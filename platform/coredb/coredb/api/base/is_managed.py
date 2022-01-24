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

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class IsManagedMixin(serializers.Serializer):
    is_managed = serializers.BooleanField(initial=True, default=True, allow_null=True)

    def _get_is_managed(self, value):
        return value if isinstance(value, bool) else True

    def check_if_entity_is_managed(self, attrs, entity_name, config_field="content"):
        cond = (
            "is_managed" in attrs
            and self._get_is_managed(attrs.get("is_managed"))
            and not attrs.get(config_field)
        )
        if cond:
            raise ValidationError(
                "{} expects a `{}`.".format(entity_name, config_field)
            )

    def validate_is_managed(self, value):
        return self._get_is_managed(value)
