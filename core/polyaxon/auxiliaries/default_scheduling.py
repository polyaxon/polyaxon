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
from typing import Any

from marshmallow import fields

from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class DefaultSchedulingSchema(BaseCamelSchema):
    node_selector = fields.Dict(allow_none=True)
    affinity = SwaggerField(cls=k8s_schemas.V1Affinity, allow_none=True)
    tolerations = fields.List(
        SwaggerField(cls=k8s_schemas.V1Toleration), allow_none=True
    )
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1DefaultScheduling


class V1DefaultScheduling(BaseConfig):
    SCHEMA = DefaultSchedulingSchema
    IDENTIFIER = "default_scheduling"
    REDUCED_ATTRIBUTES = [
        "nodeSelector",
        "affinity",
        "tolerations",
        "imagePullSecrets",
    ]

    def __init__(
        self,
        node_selector=None,
        affinity=None,
        tolerations=None,
        image_pull_secrets=None,
    ):
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations
        self.image_pull_secrets = image_pull_secrets

    @staticmethod
    def get_service_environment(
        service: Any,
        default_scheduling: "V1DefaultScheduling",
    ) -> "V1Environment":
        from polyaxon.polyflow import V1Environment

        env = V1Environment()
        if service and service.node_selector:
            env.node_selector = service.node_selector
        elif default_scheduling and default_scheduling.node_selector:
            env.node_selector = default_scheduling.node_selector
        if service and service.affinity:
            env.affinity = service.affinity
        elif default_scheduling and default_scheduling.affinity:
            env.affinity = default_scheduling.affinity
        if service and service.tolerations:
            env.tolerations = service.tolerations
        elif default_scheduling and default_scheduling.tolerations:
            env.tolerations = default_scheduling.tolerations
        if service and service.image_pull_secrets:
            env.image_pull_secrets = service.image_pull_secrets
        elif default_scheduling and default_scheduling.image_pull_secrets:
            env.image_pull_secrets = default_scheduling.image_pull_secrets

        return env
