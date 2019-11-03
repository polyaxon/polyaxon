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

from polyaxon.schemas.ops.termination import TerminationConfig


@pytest.mark.termination_mark
class TestTerminationConfigs(TestCase):
    def test_termination_config(self):
        config_dict = {}
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add max_retries
        config_dict["max_retries"] = 4
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add timeout
        config_dict["timeout"] = 4
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add restart_policy
        config_dict["restart_policy"] = "never"
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add ttl
        config_dict["ttl"] = 40
        config = TerminationConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
