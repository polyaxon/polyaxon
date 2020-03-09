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

from marshmallow import ValidationError
from tests.utils import BaseTestCase

from polyaxon.deploy.schemas.security_context import SecurityContextConfig


class TestSecurityContentConfig(BaseTestCase):
    def test_security_content_config(self):
        config_dict = {}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {"enabled": True}
        SecurityContextConfig.from_dict(config_dict)

        config_dict = {"enabled": False}
        SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {"user": "foo"}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {"user": 120}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {"group": "foo"}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {"group": 120}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {"user": "sdf", "group": 120}
            SecurityContextConfig.from_dict(config_dict)

        config_dict = {"user": 120, "group": 120}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {"enabled": True, "user": 120, "group": 120}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
