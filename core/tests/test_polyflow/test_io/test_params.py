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

from polyaxon.polyflow.params import V1Param
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.polyflow_mark
class TestV1Params(BaseTestCase):
    def test_wrong_param_config(self):
        # No name
        with self.assertRaises(ValidationError):
            V1Param.from_dict({})

    def test_wrong_param_with_ref_and_search(self):
        with self.assertRaises(ValidationError):
            V1Param.from_dict(
                {"value": "something", "ref": "test", "search": {"query": "test"}}
            )

    def test_wrong_param_without_value(self):
        with self.assertRaises(ValidationError):
            V1Param.from_dict({"ref": "test"})
        with self.assertRaises(ValidationError):
            V1Param.from_dict({"search": {"query": "test"}})

    def test_wrong_param_value_type(self):
        with self.assertRaises(ValidationError):
            V1Param.from_dict({"ref": "test", "value": 12})
        with self.assertRaises(ValidationError):
            V1Param.from_dict({"search": {"query": "test"}, "value": {"foo": "bar"}})

    def test_param_config_with_value(self):
        config_dict = {"value": "string_value"}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is True
        assert config.is_ref is False

        config_dict = {"value": 234}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is True
        assert config.is_ref is False

        config_dict = {"value": 23.4}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is True
        assert config.is_ref is False

        config_dict = {"value": {"key": "value"}}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is True
        assert config.is_ref is False

        config_dict = {"value": ["value1", "value2"]}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is True
        assert config.is_ref is False

    def test_param_ref(self):
        config_dict = {"value": "outputs", "ref": "ops.A"}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is False
        assert config.is_ref is True

        config_dict = {"value": "outputs.output1", "ref": "ops.A"}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is False
        assert config.is_ref is True

        config_dict = {
            "value": "artifact.metric_events",
            "ref": "runs.0de53b5bf8b04a219d12a39c6b92bcce",
        }
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is False
        assert config.is_ref is True

        config_dict = {"value": "input.param1", "ref": "dag"}
        config = V1Param.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        assert config.is_literal is False
        assert config.is_ref is True
