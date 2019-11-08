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

from polyaxon.schemas.cli.cli_configuration import CliConfigurationConfig


class TestCliConfig(TestCase):
    def test_cli_config(self):
        config_dict = {
            "check_count": 1,
            "current_version": "0.0.1",
            "server_versions": {"cli": "0.0.1"},
            "log_handler": None,
        }
        config = CliConfigurationConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
