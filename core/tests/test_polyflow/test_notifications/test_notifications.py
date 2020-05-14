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

import pytest

from marshmallow import ValidationError
from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon.polyflow.notifications import V1Notification


@pytest.mark.plugins_mark
class TestNotificationsConfigs(BaseTestCase):
    def test_notifications_config(self):
        # Add auth
        config_dict = {}

        with self.assertRaises(ValidationError):
            V1Notification.from_dict(config_dict)

        # Add connection
        config_dict["connections"] = ["test"]
        config = V1Notification.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add a trigger policy
        config_dict["trigger"] = "not-supported"
        with self.assertRaises(ValidationError):
            V1Notification.from_dict(config_dict)

        # Add outputs
        config_dict["trigger"] = "succeeded"
        config = V1Notification.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
