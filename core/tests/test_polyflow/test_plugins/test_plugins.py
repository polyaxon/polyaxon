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

from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon.polyflow.plugins import V1Plugins


@pytest.mark.plugins_mark
class TestPluginsConfigs(BaseTestCase):
    def test_plugins_config(self):
        # Add auth
        config_dict = {"auth": True}

        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add docker
        config_dict["docker"] = True
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add shm
        config_dict["shm"] = True
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add outputs
        config_dict["collectArtifacts"] = True
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add logs
        config_dict["collectLogs"] = True
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add resources
        config_dict["collectResources"] = True
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add notifications
        config_dict["notifications"] = [
            {"connections": ["test1"], "trigger": "succeeded"},
            {"connections": ["test2"], "trigger": "failed"},
            {"connections": ["test3"], "trigger": "done"},
        ]
        config = V1Plugins.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
