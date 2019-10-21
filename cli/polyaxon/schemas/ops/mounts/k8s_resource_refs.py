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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
import warnings

from marshmallow import ValidationError, fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class K8SResourceRefSchema(BaseSchema):
    name = fields.Str()
    mount_path = fields.Str(allow_none=True)
    items = RefOrObject(fields.List(fields.Str(), allow_none=True))

    @staticmethod
    def schema_config():
        return K8SResourceRefConfig


class K8SResourceRefConfig(BaseConfig):
    IDENTIFIER = "k8s_resource_ref"
    SCHEMA = K8SResourceRefSchema
    REDUCED_ATTRIBUTES = ["name", "mount_path", "items"]

    def __init__(self, name, mount_path=None, items=None):
        self.name = name
        self.mount_path = mount_path
        self.items = items


def validate_resource_refs(values, field):
    field_value = values.get(field)
    if not field_value:
        return values
    field_value = [
        {"name": v} if isinstance(v, six.string_types) else v for v in field_value
    ]
    for v in field_value:
        try:
            K8SResourceRefSchema(unknown=BaseConfig.UNKNOWN_BEHAVIOUR).load(v)
        except ValidationError:
            raise ValidationError(
                "K8S Resource field `{}` is not a valid value.".format(v)
            )
    values[field] = field_value
    return values


def validate_config_map_refs(values):
    if values.get("config_map_refs") and values.get("configmap_refs"):
        raise ValidationError("You should only use `config_map_refs`.")

    if values.get("configmap_refs"):
        warnings.warn(
            "The `configmap_refs` parameter is deprecated and will be removed in next release, "
            "please use `config_map_refs` instead.",
            DeprecationWarning,
        )
        values["config_map_refs"] = values.pop("configmap_refs")

    return validate_resource_refs(values=values, field="config_map_refs")


def validate_secret_refs(values):
    return validate_resource_refs(values=values, field="secret_refs")
