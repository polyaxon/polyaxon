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

from polyaxon.polyaxonfile.specs.libs.parser import Parser
from polyaxon.polyflow.operators import ForConfig, IfConfig
from tests.utils import BaseTestCase


@pytest.mark.polyflow_mark
class TestOperatorConfigs(BaseTestCase):
    def test_for_operator_config(self):
        config_dict = {"len": 5, "do": "Value at {{ i }}", "index": "i"}
        config = ForConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        expected = [
            "Value at 0",
            "Value at 1",
            "Value at 2",
            "Value at 3",
            "Value at 4",
        ]
        assert expected == config.parse(Parser(), {})

        config_dict = {
            "len": 5,
            "do": [
                {"Conv2D": {"strides": ["{{ i }}", "{{ i }}"]}},
                {"Pooling2D": {"strides": ["{{ i }}", "{{ i }}"]}},
            ],
            "index": "i",
        }
        config = ForConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Lists get flattened
        expected = [
            {"Conv2D": {"strides": [0, 0]}},
            {"Pooling2D": {"strides": [0, 0]}},
            {"Conv2D": {"strides": [1, 1]}},
            {"Pooling2D": {"strides": [1, 1]}},
            {"Conv2D": {"strides": [2, 2]}},
            {"Pooling2D": {"strides": [2, 2]}},
            {"Conv2D": {"strides": [3, 3]}},
            {"Pooling2D": {"strides": [3, 3]}},
            {"Conv2D": {"strides": [4, 4]}},
            {"Pooling2D": {"strides": [4, 4]}},
        ]
        assert expected == config.parse(Parser(), {})

    def test_if_operator_config(self):
        config_dict = {
            "cond": "{{ i }} == 5",
            "do": "It was True",
            "elseDo": "It was False",
        }
        config = IfConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert "It was True" == config.parse(Parser(), {"i": 5})
        assert "It was False" == config.parse(Parser(), {"i": 3})
