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

from marshmallow import EXCLUDE, fields

from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class BaseServiceSchema(BaseCamelSchema):
    image = fields.Str(allow_none=True)
    image_tag = fields.Str(allow_none=True)
    image_pull_policy = fields.Str(allow_none=True)
    resources = SwaggerField(cls=k8s_schemas.V1ResourceRequirements, allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    affinity = SwaggerField(cls=k8s_schemas.V1Affinity, allow_none=True)
    tolerations = fields.List(
        SwaggerField(cls=k8s_schemas.V1Toleration), allow_none=True
    )
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @staticmethod
    def schema_config():
        return BaseServiceConfig


class BaseServiceConfig(BaseConfig):
    SCHEMA = BaseServiceSchema
    REDUCED_ATTRIBUTES = [
        "image",
        "imageTag",
        "imagePullPolicy",
        "resources",
        "nodeSelector",
        "affinity",
        "tolerations",
        "imagePullSecrets",
    ]

    def __init__(
        self,
        image=None,
        image_tag=None,
        image_pull_policy=None,
        resources=None,
        node_selector=None,
        affinity=None,
        tolerations=None,
        image_pull_secrets=None,
    ):
        self.image = image
        self.image_tag = image_tag
        self.image_pull_policy = image_pull_policy
        self.resources = resources
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations
        self.image_pull_secrets = image_pull_secrets
