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

import polyaxon_sdk

from marshmallow import fields

from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class EnvironmentSchema(BaseCamelSchema):
    labels = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    annotations = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    node_selector = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    affinity = SwaggerField(cls=k8s_schemas.V1Affinity, allow_none=True)
    tolerations = fields.List(
        SwaggerField(cls=k8s_schemas.V1Toleration), allow_none=True
    )
    node_name = fields.Str(allow_none=True)
    service_account_name = fields.Str(allow_none=True)
    host_aliases = fields.List(
        SwaggerField(cls=k8s_schemas.V1HostAlias), allow_none=True
    )
    security_context = SwaggerField(cls=k8s_schemas.V1SecurityContext, allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    host_network = fields.Bool(allow_none=True)
    dns_policy = fields.Str(allow_none=True)
    dns_config = SwaggerField(cls=k8s_schemas.V1PodDNSConfig, allow_none=True)
    scheduler_name = fields.Str(allow_none=True)
    priority_class_name = fields.Str(allow_none=True)
    priority = fields.Int(allow_none=True)
    restart_policy = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1Environment


class V1Environment(BaseConfig, polyaxon_sdk.V1Environment):
    """
    Pod environment config.
    """

    IDENTIFIER = "environment"
    SCHEMA = EnvironmentSchema
    REDUCED_ATTRIBUTES = [
        "labels",
        "annotations",
        "nodeSelector",
        "affinity",
        "tolerations",
        "nodeName",
        "serviceAccountName",
        "hostAliases",
        "securityContext",
        "imagePullSecrets",
        "hostNetwork",
        "dnsPolicy",
        "dnsConfig",
        "schedulerName",
        "priorityClassName",
        "priority",
        "restartPolicy",
    ]
