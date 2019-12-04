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

from polyaxon.schemas.polyflow.init import InitConfig


@pytest.mark.init_mark
class TestInitConfigs(TestCase):
    def test_init_config(self):
        config_dict = {}
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add artifacts
        config_dict["artifacts"] = [
            {"name": "data2"},
            {"name": "data3", "paths": ["/subpath1", "subpath2"]},
            {"name": "artifact2", "paths": ["/subpath1", "subpath2"]},
        ]
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add repos
        config_dict["repos"] = [
            {"name": "repo1"},
            {"name": "repo1", "commit": "commit-hash"},
            {"name": "repo2", "branch": "dev"},
        ]
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add build context
        config_dict = {
            "build": {
                "image": "tensorflow:1.3.0",
                "run": ["pip install tensor2tensor"],
                "env": [["LC_ALL", "en_US.UTF-8"]],
                "shell": "foo",
                "name": "foo.yaml",
                "workdir": "/test",
            }
        }
        config = InitConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
