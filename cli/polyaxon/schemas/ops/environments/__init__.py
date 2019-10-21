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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.ops.environments.container_resources import (
    ContainerResourcesSchema,
)
from polyaxon.schemas.ops.environments.containers import ContainerSchema


class EnvironmentSchema(BaseSchema):
    resources = fields.Nested(ContainerResourcesSchema, allow_none=True)
    labels = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    annotations = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    node_selector = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(), allow_none=True)
    service_account = fields.Str(allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    security_context = fields.Dict(allow_none=True)
    log_level = fields.Str(allow_none=True)
    auth = fields.Bool(allow_none=True)
    docker = fields.Bool(allow_none=True)
    shm = fields.Bool(allow_none=True)
    outputs = fields.Bool(allow_none=True)
    logs = fields.Bool(allow_none=True)
    registry = fields.Str(allow_none=True)
    init_container = fields.Nested(ContainerSchema, allow_none=True)
    sidecar_container = fields.Nested(ContainerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return EnvironmentConfig


class EnvironmentConfig(BaseConfig):
    """
    Pod environment config.
    """

    IDENTIFIER = "environment"
    SCHEMA = EnvironmentSchema
    REDUCED_ATTRIBUTES = [
        "resources",
        "labels",
        "annotations",
        "node_selector",
        "affinity",
        "tolerations",
        "service_account",
        "image_pull_secrets",
        "env_vars",
        "security_context",
        "log_level",
        "auth",
        "docker",
        "shm",
        "outputs",
        "logs",
        "registry",
        "init_container",
        "sidecar_container",
    ]

    def __init__(
        self,
        resources=None,
        labels=None,
        annotations=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
        service_account=None,
        image_pull_secrets=None,
        env_vars=None,
        security_context=None,
        log_level=None,
        docker=None,
        shm=None,
        auth=None,
        outputs=None,
        logs=None,
        registry=None,
        init_container=None,
        sidecar_container=None,
    ):
        self.resources = resources
        self.labels = labels
        self.annotations = annotations
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations
        self.service_account = service_account
        self.image_pull_secrets = image_pull_secrets
        self.env_vars = env_vars
        self.security_context = security_context
        self.log_level = log_level
        self.docker = docker
        self.shm = shm
        self.auth = auth
        self.outputs = outputs
        self.logs = logs
        self.registry = registry
        self.init_container = init_container
        self.sidecar_container = sidecar_container
