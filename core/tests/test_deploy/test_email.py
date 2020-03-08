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

from polyaxon.deploy.schemas.email import EmailConfig


class TestEmailConfig(BaseTestCase):
    def test_email_config(self):
        config_dict = {
            "host": "dsf",
            "port": "sdf",
            "useTls": 123,
            "hostUser": "sdf",
            "hostPassword": "sdf",
        }
        with self.assertRaises(ValidationError):
            EmailConfig.from_dict(config_dict)

        config_dict = {
            "host": "dsf",
            "port": 123,
            "useTls": False,
            "hostUser": "sdf",
            "hostPassword": "sdf",
        }
        config = EmailConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
