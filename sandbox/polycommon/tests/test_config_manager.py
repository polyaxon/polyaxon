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

import os

from unittest import TestCase

from polyaxon.exceptions import PolyaxonSchemaError
from polycommon.config_manager import ConfigManager


class TestConfigManager(TestCase):
    def test_get_from_os_env(self):
        os.environ["POLYAXON_ENVIRONMENT"] = "testing"
        os.environ["FOO_BAR_KEY"] = "foo_bar"
        config = ConfigManager.read_configs(
            [os.environ, "./tests/fixtures_static/configs/non_opt_config_tests.json"]
        )

        assert config.get_string("POLYAXON_ENVIRONMENT") == "testing"
        assert config.get_string("FOO_BAR_KEY") == "foo_bar"

    def test_raises_for_non_optional_env_vars(self):
        with self.assertRaises(PolyaxonSchemaError):
            ConfigManager.read_configs([os.environ])

    def test_get_broker(self):
        os.environ["POLYAXON_ENVIRONMENT"] = "testing"
        os.environ.pop("POLYAXON_BROKER_BACKEND", None)
        config = ConfigManager.read_configs(
            [os.environ, "./tests/fixtures_static/configs/non_opt_config_tests.json"]
        )
        assert config.broker_backend == "rabbitmq"
        assert config.is_redis_broker is False
        assert config.is_rabbitmq_broker is True

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {"POLYAXON_BROKER_BACKEND": "rabbitmq"},
            ]
        )
        assert config.broker_backend == "rabbitmq"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {"POLYAXON_BROKER_BACKEND": "redis"},
            ]
        )
        assert config.broker_backend == "redis"
        assert config.is_redis_broker is True
        assert config.is_rabbitmq_broker is False

    def test_get_broker_url(self):
        os.environ["POLYAXON_ENVIRONMENT"] = "testing"
        os.environ.pop("POLYAXON_RABBITMQ_USER", None)
        os.environ.pop("POLYAXON_RABBITMQ_PASSWORD", None)
        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_BROKER_BACKEND": "redis",
                    "POLYAXON_REDIS_CELERY_BROKER_URL": "foo",
                },
            ]
        )
        assert config.get_broker_url() == "redis://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_REDIS_PROTOCOL": "rediss",
                    "POLYAXON_BROKER_BACKEND": "redis",
                    "POLYAXON_REDIS_CELERY_BROKER_URL": "foo",
                },
            ]
        )
        assert config.get_broker_url() == "rediss://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_BROKER_BACKEND": "redis",
                    "POLYAXON_REDIS_CELERY_BROKER_URL": "foo",
                    "POLYAXON_REDIS_PASSWORD": "pass",
                },
            ]
        )
        assert config.get_broker_url() == "redis://:pass@foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_AMQP_URL": "foo",
                    "POLYAXON_BROKER_BACKEND": "rabbitmq",
                    "POLYAXON_REDIS_CELERY_BROKER_URL": "foo",
                },
            ]
        )
        assert config.get_broker_url() == "amqp://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_AMQP_URL": "foo",
                    "POLYAXON_BROKER_BACKEND": "rabbitmq",
                    "POLYAXON_RABBITMQ_PASSWORD": "",
                    "POLYAXON_REDIS_CELERY_BROKER_URL": "foo",
                },
            ]
        )
        assert config.get_broker_url() == "amqp://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_AMQP_URL": "foo",
                    "POLYAXON_BROKER_BACKEND": "rabbitmq",
                    "POLYAXON_RABBITMQ_PASSWORD": "",
                    "POLYAXON_RABBITMQ_USER": "user",
                },
            ]
        )
        assert config.get_broker_url() == "amqp://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_AMQP_URL": "foo",
                    "POLYAXON_BROKER_BACKEND": "rabbitmq",
                    "POLYAXON_RABBITMQ_USER": "",
                    "POLYAXON_RABBITMQ_PASSWORD": "pwd",
                },
            ]
        )
        assert config.get_broker_url() == "amqp://foo"

        config = ConfigManager.read_configs(
            [
                os.environ,
                "./tests/fixtures_static/configs/non_opt_config_tests.json",
                {
                    "POLYAXON_AMQP_URL": "foo",
                    "POLYAXON_BROKER_BACKEND": "rabbitmq",
                    "POLYAXON_RABBITMQ_USER": "user",
                    "POLYAXON_RABBITMQ_PASSWORD": "pwd",
                },
            ]
        )
        assert config.get_broker_url() == "amqp://user:pwd@foo"
