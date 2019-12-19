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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow.exceptions import ValidationError

from polyaxon.config_resources.kinds import ConfigResourceKind
from polyaxon.config_resources.schemas import ConfigResourceConfig, validate_config_resource


class TestConfigResourceConfig(TestCase):
    def test_claim_connect_config(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            ConfigResourceConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            validate_config_resource(ConfigResourceKind.SERVICE_ACCOUNT, config_dict)

        config_dict = {"ref": "sdf"}
        ConfigResourceConfig.from_dict(config_dict)
        validate_config_resource(ConfigResourceKind.SERVICE_ACCOUNT, config_dict)

        config_dict = {"ref": "sdf", "items": ["foo"], "mount_path": "/bar"}
        config = ConfigResourceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        validate_config_resource(ConfigResourceKind.SERVICE_ACCOUNT, config_dict)
