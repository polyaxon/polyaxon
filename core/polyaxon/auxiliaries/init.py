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
from polyaxon.containers.pull_policy import PullPolicy
from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


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
    """Polyaxon init is a helper container that initialize the environment
    required for the main container to function correctly.

    Polyaxon CE and Polyaxon Agent are deployed with default values for the init container,
    however if you need to control or update one or several aspects
    of how the init container that gets injected, this guide walks through the possible options.

    Args:
        image: str, optional.
        image_tag: str, optional.
        image_pull_policy: str, optional.
        resources: V1ResourceRequirements, optional.

    ## YAML usage

    ```yaml
    >>> init:
    >>>   image: polyaxon/polyaxon-sidecar
    >>>   imageTag: v1.x
    >>>   imagePullPolicy: IfNotPresent
    >>>   resources: requests:
    >>>     memory: "64Mi"
    >>>     cpu: "50m"
    ```

    ## Fields

    ### image

    The container image to use.

    ```yaml
    >>> init:
    >>>   image: polyaxon/polyaxon-sidecar
    ```

    ### imageTag

    The container image tag to use.

    ```yaml
    >>> init:
    >>>   imageTag: dev
    ```

    ### imagePullPolicy

    The image pull policy to use, it must be a valid policy supported by Kubernetes.

    ```yaml
    >>> init:
    >>>   imagePullPolicy: Always
    ```

    ### resources

    The resources requirements to allocate to the container.

    ```yaml
    >>> init:
    >>>   resources:
    >>>     memory: "64Mi"
    >>>     cpu: "50m"
    ```

    > **N.B.1**: That this resources are applied to all instances of
    the init container within the same pod.

    > **N.B.2**: It's possible to alter this behaviour on per operation level
        using the init section.
    """

    SCHEMA = PolyaxonInitContainerSchema
    IDENTIFIER = "container"
    REDUCED_ATTRIBUTES = ["imageTag", "imagePullPolicy", "resources"]

    def get_image(self):
        image = self.image or "polyaxon/polyaxon-init"
        image_tag = self.image_tag if self.image_tag is not None else pkg.VERSION
        return "{}:{}".format(image, image_tag) if image_tag else image

    def get_resources(self):
        return self.resources if self.resources else get_init_resources()


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
