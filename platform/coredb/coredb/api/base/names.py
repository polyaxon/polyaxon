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

from rest_framework.exceptions import ValidationError


class NamesMixin:
    def validated_name(self, validated_data, project, query):
        name = validated_data.get("name")
        if name and query.filter(project=project, name=name).exists():
            count = query.exclude(name=name).filter(name__startswith=name).count() + 1
            validated_data["name"] = "{}-{}".format(name, count)
        return validated_data


class CatalogNamesMixin:
    def validated_name(self, validated_data, owner, query):
        name = validated_data.get("name")
        if name and query.filter(owner=owner, name=name).exists():
            raise ValidationError("An instance already exists with this name.")
        return validated_data
