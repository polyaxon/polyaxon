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

import numpy as np
import os

from collections.abc import Mapping
from unittest import TestCase, mock

import ujson

from polyaxon import settings
from polyaxon.schemas.api.authentication import AccessTokenConfig
from polyaxon.schemas.cli.agent_config import AgentConfig
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.schemas.cli.proxies_config import ProxiesConfig


def assert_equal_dict(dict1, dict2):
    for k, v in dict1.items():
        if v is None:
            continue
        if isinstance(v, Mapping):
            assert_equal_dict(v, dict2[k])
        else:
            assert v == dict2[k]


def assert_equal_feature_processors(fp1, fp2):
    # Check that they have same features
    assert list(fp1.keys()) == list(fp2.key())

    # Check that all features have the same graph
    for feature in fp1:
        assert_equal_graphs(fp2[feature], fp1[feature])


def assert_tensors(tensor1, tensor2):
    if isinstance(tensor1, str):
        tensor1 = [tensor1, 0, 0]

    if isinstance(tensor2, str):
        tensor2 = [tensor2, 0, 0]

    assert tensor1 == tensor2


def assert_equal_graphs(result_graph, expected_graph):
    for i, input_layer in enumerate(expected_graph["input_layers"]):
        assert_tensors(input_layer, result_graph["input_layers"][i])

    for i, output_layer in enumerate(expected_graph["output_layers"]):
        assert_tensors(output_layer, result_graph["output_layers"][i])

    for layer_i, layer in enumerate(result_graph["layers"]):
        layer_name, layer_data = list(layer.items())[0]
        assert layer_name in expected_graph["layers"][layer_i]
        for k, v in layer_data.items():
            assert v == expected_graph["layers"][layer_i][layer_name][k]


def assert_equal_layers(config, expected_layer):
    result_layer = config.to_dict()
    for k, v in expected_layer.items():
        if v is not None or k not in config.REDUCED_ATTRIBUTES:
            assert v == result_layer[k]
        else:
            assert k not in result_layer


def patch_settings(
    set_auth: bool = True,
    set_client: bool = True,
    set_agent: bool = True,
    set_proxies: bool = True,
):
    settings.AUTH_CONFIG = None
    if set_auth:
        settings.AUTH_CONFIG = AccessTokenConfig()

    settings.CLIENT_CONFIG = None
    if set_client:
        settings.CLIENT_CONFIG = ClientConfig(host="1.2.3.4")

    settings.AGENT_CONFIG = None
    if set_agent:
        settings.AGENT_CONFIG = AgentConfig()

    settings.PROXIES_CONFIG = None
    if set_proxies:
        settings.PROXIES_CONFIG = ProxiesConfig()

    settings.CLIENT_CONFIG.tracking_timeout = 0


class BaseTestCase(TestCase):
    SET_AUTH_SETTINGS = True
    SET_CLIENT_SETTINGS = True
    SET_AGENT_SETTINGS = False
    SET_PROXIES_SETTINGS = False

    def setUp(self):
        super().setUp()
        patch_settings(
            set_auth=self.SET_AUTH_SETTINGS,
            set_client=self.SET_CLIENT_SETTINGS,
            set_agent=self.SET_AGENT_SETTINGS,
            set_proxies=self.SET_PROXIES_SETTINGS,
        )


class TestEnvVarsCase(BaseTestCase):
    @staticmethod
    def check_empty_value(key, expected_function):
        os.environ.pop(key, None)
        assert expected_function() is None

    @staticmethod
    def check_non_dict_value(key, expected_function, value="non dict random value"):
        os.environ[key] = value
        assert expected_function() is None

    @staticmethod
    def check_valid_dict_value(key, expected_function, value):
        os.environ[key] = ujson.dumps(value)
        assert expected_function() == value

    def check_raise_for_invalid_value(self, key, expected_function, value, exception):
        os.environ[key] = ujson.dumps(value)
        with self.assertRaises(exception):
            expected_function()

    @staticmethod
    def check_valid_value(key, expected_function, value, expected_value=None):
        os.environ[key] = value
        expected_value = expected_value or value
        assert expected_function() == expected_value


def tensor_np(shape, dtype=float):
    return np.arange(np.prod(shape), dtype=dtype).reshape(shape)


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)
