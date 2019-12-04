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

import pytest

from tests.utils import assert_equal_dict

from polyaxon.schemas.polyflow.environment import EnvironmentConfig


@pytest.mark.environment_mark
class TestEnvironmentsConfigs(TestCase):
    def test_environment_resources(self):
        config_dict = {
            "resources": {
                "requests": {
                    "cpu": 0.5,
                    "memory": "256Mi",
                    "nvidia.com/gpu": 1,
                    "amd.com/gpu": 2,
                },
                "limits": {
                    "cpu": 1,
                    "memory": "400Mi",
                    "nvidia.com/gpu": 1,
                    "amd.com/gpu": 2,
                },
            }
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_environment_config(self):
        # Resources
        config_dict = {
            "resources": {
                "requests": {"cpu": 0.5, "memory": "256Mi"},
                "limits": {"cpu": 1, "memory": "400Mi"},
            }
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add node selectors
        config_dict["node_selector"] = {"polyaxon.com": "master"}

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add affinity
        config_dict["affinity"] = {
            "nodeAffinity": {"requiredDuringSchedulingIgnoredDuringExecution": {}}
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add labels
        config_dict["labels"] = {"foo": "bar"}

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add annotations
        config_dict["annotations"] = {"foo": "bar"}

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add toleration
        config_dict["tolerations"] = [{"key": "key", "operator": "Exists"}]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add service_account
        config_dict["service_account"] = "service_account"
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add image_pull_secrets
        config_dict["image_pull_secrets"] = ["pull_secret1", "pull_secret2"]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add env vars
        config_dict["env_vars"] = {"key": "value"}
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add security context per job
        config_dict["security_context"] = {
            "runAsUser": 1000,
            "runAsGroup": 3000,
            "fsGroup": 5000,
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add security context per job
        config_dict["log_level"] = "INFO"
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add auth
        config_dict["auth"] = True
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add docker
        config_dict["docker"] = True
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add shm
        config_dict["shm"] = True
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add outputs
        config_dict["outputs"] = True
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add logs
        config_dict["logs"] = True
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add registry
        config_dict["registry"] = "foo"
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
