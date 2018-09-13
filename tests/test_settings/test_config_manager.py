import os

from rhea import RheaError

import pytest

from polyaxon.config_manager import ConfigManager
from tests.utils import BaseTest


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
