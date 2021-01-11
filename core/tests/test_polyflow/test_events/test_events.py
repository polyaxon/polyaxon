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

import pytest

from marshmallow import ValidationError

from polyaxon.polyflow import V1EventKind, V1EventTrigger
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.events_mark
class TestEventTriggerConfigs(BaseTestCase):
    def test_events_config(self):
        config_dict = {}

        with self.assertRaises(ValidationError):
            V1EventTrigger.from_dict(config_dict)

        config_dict["ref"] = "test"
        with self.assertRaises(ValidationError):
            V1EventTrigger.from_dict(config_dict)

        # Add kinds
        config_dict["kinds"] = [V1EventKind.RUN_STATUS_DONE]
        config = V1EventTrigger.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Set correct ref
        config_dict["ref"] = "ops.A"
        config = V1EventTrigger.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add another event
        config_dict["kinds"] = [
            V1EventKind.RUN_STATUS_RESUMING,
            V1EventKind.RUN_NEW_ARTIFACTS,
        ]
        V1EventTrigger.from_dict(config_dict)

        # Use run event
        config_dict["ref"] = "runs.0de53b5bf8b04a219d12a39c6b92bcce"
        config = V1EventTrigger.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
