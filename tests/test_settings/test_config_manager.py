import os

import pytest

from rhea import RheaError

from polyaxon.config_manager import ConfigManager
from tests.base.case import BaseTest


@pytest.mark.settings_mark
class TestConfigManager(BaseTest):
    def test_get_from_os_env(self):
        os.environ['POLYAXON_ENVIRONMENT'] = 'testing'
        os.environ['FOO_BAR_KEY'] = 'foo_bar'
        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json'])

        assert config.get_string('POLYAXON_ENVIRONMENT') == 'testing'
        assert config.get_string('FOO_BAR_KEY') == 'foo_bar'

    def test_raises_for_non_optional_env_vars(self):
        with self.assertRaises(RheaError):
            ConfigManager.read_configs([os.environ])

    def test_get_broker(self):
        os.environ['POLYAXON_ENVIRONMENT'] = 'testing'
        config = ConfigManager.read_configs(
            [os.environ, './tests/fixtures_static/configs/non_opt_config_tests.json'])
        assert config.broker_backend == 'rabbitmq'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_BROKER_BACKEND': 'rabbitmq'}])
        assert config.broker_backend == 'rabbitmq'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_BROKER_BACKEND': 'redis'}])
        assert config.broker_backend == 'redis'

    def test_get_broker_url(self):
        os.environ['POLYAXON_ENVIRONMENT'] = 'testing'
        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_BROKER_BACKEND': 'redis',
              'POLYAXON_REDIS_CELERY_BROKER_URL': 'foo'}])
        assert config.get_broker_url() == 'redis://foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_BROKER_BACKEND': 'redis',
              'POLYAXON_REDIS_CELERY_BROKER_URL': 'foo',
              'POLYAXON_REDIS_PASSWORD': 'pass'}])
        assert config.get_broker_url() == 'redis://:pass@foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_AMQP_URL': 'foo',
              'POLYAXON_REDIS_CELERY_BROKER_URL': 'foo'}])
        assert config.get_broker_url() == 'amqp://polyaxon:polyaxon@foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_AMQP_URL': 'foo',
              'POLYAXON_RABBITMQ_PASSWORD': '',
              'POLYAXON_REDIS_CELERY_BROKER_URL': 'foo'}])
        assert config.get_broker_url() == 'amqp://foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_AMQP_URL': 'foo',
              'POLYAXON_RABBITMQ_PASSWORD': '',
              'POLYAXON_RABBITMQ_USER': 'user'}])
        assert config.get_broker_url() == 'amqp://foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_AMQP_URL': 'foo',
              'POLYAXON_RABBITMQ_USER': '',
              'POLYAXON_RABBITMQ_PASSWORD': 'pwd'}])
        assert config.get_broker_url() == 'amqp://foo'

        config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/non_opt_config_tests.json',
             {'POLYAXON_AMQP_URL': 'foo',
              'POLYAXON_RABBITMQ_USER': 'user',
              'POLYAXON_RABBITMQ_PASSWORD': 'pwd'}])
        assert config.get_broker_url() == 'amqp://user:pwd@foo'
