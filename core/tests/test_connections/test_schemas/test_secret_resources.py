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

from marshmallow.exceptions import ValidationError
from tests.utils import BaseTestCase

from polyaxon.connections.schemas import V1K8sResourceSchema, validate_k8s_resource


class TestSecretResourceValidation(BaseTestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            V1K8sResourceSchema.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_k8s_resource(config_dict)

        config_dict = {"name": "sdf"}
        V1K8sResourceSchema.from_dict(config_dict)
        validate_k8s_resource(config_dict)

        config_dict = {"name": "sdf", "items": ["foo"], "mountPath": "/bar"}
        config = V1K8sResourceSchema.from_dict(config_dict)
        assert config.to_dict() == config_dict
        validate_k8s_resource(config_dict)
