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

from polyaxon import pkg
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.containers.pull_policy import PullPolicy
from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


def get_sidecar_resources() -> k8s_schemas.V1ResourceRequirements:
    return k8s_schemas.V1ResourceRequirements(
        limits={"cpu": "1", "memory": "100Mi"},
        requests={"cpu": "0.1", "memory": "60Mi"},
    )


class PolyaxonSidecarContainerSchema(BaseCamelSchema):
    image = fields.Str(required=True)
    image_tag = fields.Str(required=True)
    image_pull_policy = fields.Str(allow_none=True)
    resources = SwaggerField(cls=k8s_schemas.V1ResourceRequirements, allow_none=True)
    sleep_interval = fields.Int(allow_none=True)
    sync_interval = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return V1PolyaxonSidecarContainer


class V1PolyaxonSidecarContainer(BaseConfig, polyaxon_sdk.V1PolyaxonSidecarContainer):
    SCHEMA = PolyaxonSidecarContainerSchema
    IDENTIFIER = "polyaxon_sidecar"
    REDUCED_ATTRIBUTES = [
        "imageTag",
        "imagePullPolicy",
        "sleepInterval",
        "resources",
        "syncInterval",
    ]

    def get_image(self):
        image = self.image or "polyaxon/polyaxon-sidecar"
        image_tag = self.image_tag if self.image_tag is not None else pkg.VERSION
        return "{}:{}".format(image, image_tag) if image_tag else image

    def get_resources(self):
        return self.resources if self.resources else get_sidecar_resources()


def get_init_resources() -> k8s_schemas.V1ResourceRequirements:
    return k8s_schemas.V1ResourceRequirements(
        limits={"cpu": "1", "memory": "200Mi"},
        requests={"cpu": "0.1", "memory": "20Mi"},
    )


class PolyaxonInitContainerSchema(BaseCamelSchema):
    image = fields.Str(required=True)
    image_tag = fields.Str(required=True)
    image_pull_policy = fields.Str(allow_none=True)
    resources = SwaggerField(cls=k8s_schemas.V1ResourceRequirements, allow_none=True)

    @staticmethod
    def schema_config():
        return V1PolyaxonInitContainer


class V1PolyaxonInitContainer(BaseConfig, polyaxon_sdk.V1PolyaxonInitContainer):
    SCHEMA = PolyaxonInitContainerSchema
    IDENTIFIER = "container"
    REDUCED_ATTRIBUTES = ["imageTag", "imagePullPolicy", "resources"]

    def get_image(self):
        image = self.image or "polyaxon/polyaxon-init"
        image_tag = self.image_tag if self.image_tag is not None else pkg.VERSION
        return "{}:{}".format(image, image_tag) if image_tag else image

    def get_resources(self):
        return self.resources if self.resources else get_init_resources()


def get_default_sidecar_container(schema=True):
    default = {
        "image": "polyaxon/polyaxon-sidecar",
        "imageTag": pkg.VERSION,
        "imagePullPolicy": PullPolicy.ALWAYS.value,
        "resources": {
            "limits": {"cpu": "1", "memory": "100Mi"},
            "requests": {"cpu": "0.1", "memory": "60Mi"},
        },
        "sleepInterval": 5,
        "syncInterval": -1,
    }
    if schema:
        return V1PolyaxonSidecarContainer.from_dict(default)
    return default


def get_default_init_container(schema=True):
    default = {
        "image": "polyaxon/polyaxon-init",
        "imageTag": pkg.VERSION,
        "imagePullPolicy": PullPolicy.ALWAYS.value,
        "resources": {
            "limits": {"cpu": "1", "memory": "200Mi"},
            "requests": {"cpu": "0.1", "memory": "20Mi"},
        },
    }
    if schema:
        return V1PolyaxonInitContainer.from_dict(default)
    return default


def get_default_notification_container():
    return V1Container(
        name=MAIN_JOB_CONTAINER,
        image="polyaxon/polyaxon-events-handlers:{}".format("dev"),
        image_pull_policy=PullPolicy.ALWAYS.value,
        command=["polyaxon", "notify"],
        args=[
            "--kind={{kind}}",
            "--owner={{owner}}",
            "--project={{project}}",
            "--run_uuid={{run_uuid}}",
            "--run_name={{run_name}}",
            "--condition={{condition}}",
        ],
        resources=k8s_schemas.V1ResourceRequirements(
            limits={"cpu": "0.5", "memory": "100Mi"},
            requests={"cpu": "0.1", "memory": "20Mi"},
        ),
    )


def get_default_tuner_container(command):
    return V1Container(
        name=MAIN_JOB_CONTAINER,
        image="polyaxon/polyaxon-hpsearch:{}".format("dev"),
        image_pull_policy=PullPolicy.ALWAYS.value,
        command=command,
        args=["--matrix={{matrix}}", "--configs={{configs}}", "--metrics={{metrics}}",],
        resources=k8s_schemas.V1ResourceRequirements(
            requests={"cpu": "0.1", "memory": "180Mi"},
        ),
    )
