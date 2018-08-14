import os

import pytest

from config_manager.config_manager import ConfigManager
from config_manager.exceptions import ConfigurationError
from tests.utils import BaseTest


@pytest.mark.config_manager_mark
class TestConfigManager(BaseTest):
    def setUp(self):
        os.environ['POLYAXON_ENVIRONMENT'] = 'testing'
        os.environ['FOO_BAR_KEY'] = 'foo_bar'
        self.config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/config_tests.json',
             './tests/fixtures_static/configs/non_opt_config_tests.json'])

    def test_get_from_os_env(self):
        assert self.config.get_string('POLYAXON_ENVIRONMENT') == 'testing'
        assert self.config.get_string('FOO_BAR_KEY') == 'foo_bar'

    def test_raises_for_non_optional_env_vars(self):
        with self.assertRaises(ConfigurationError):
            self.config = ConfigManager.read_configs(
                [os.environ,
                 './tests/fixtures_static/configs/config_tests.json'])

    def test_reading_invalid_config_raises_error(self):
        with pytest.raises(ConfigurationError):
            ConfigManager.read_configs(
                ['./tests/fixtures_static/configs/invalid_config_tests.json'])

    def test_get_boolean(self):
        value = self.config.get_boolean('bool_key_1')
        self.assertEqual(value, True)

        value = self.config.get_boolean('bool_key_2')
        self.assertEqual(value, True)

        value = self.config.get_boolean('bool_key_3')
        self.assertEqual(value, False)

        value = self.config.get_boolean('bool_key_4')
        self.assertEqual(value, False)

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_error_key_4')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_error_key_5')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_non_existing_key')

        assert self.config.get_boolean(
            'bool_non_existing_key', is_optional=True) is None
        assert self.config.get_boolean(
            'bool_non_existing_key', is_optional=True, default=True) is True

    def test_get_int(self):
        value = self.config.get_int('int_key_1')
        self.assertEqual(value, 123)

        value = self.config.get_int('int_key_2')
        self.assertEqual(value, 123)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_non_existing_key')

        assert self.config.get_boolean(
            'int_non_existing_key', is_optional=True) is None
        assert self.config.get_boolean(
            'int_non_existing_key', is_optional=True, default=34) == 34

    def test_get_float(self):
        value = self.config.get_float('float_key_1')
        self.assertEqual(value, 1.23)

        value = self.config.get_float('float_key_2')
        self.assertEqual(value, 1.23)

        value = self.config.get_float('float_key_3')
        self.assertEqual(value, 123)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_4')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_non_existing_key')

        assert self.config.get_boolean(
            'float_non_existing_key', is_optional=True) is None
        assert self.config.get_boolean(
            'float_non_existing_key', is_optional=True, default=3.4) == 3.4

    def test_get_string(self):
        value = self.config.get_string('string_key_1')
        self.assertEqual(value, "123")

        value = self.config.get_string('string_key_2')
        self.assertEqual(value, "1.23")

        value = self.config.get_string('string_key_3')
        self.assertEqual(value, "foo")

        value = self.config.get_string('string_key_4')
        self.assertEqual(value, "")

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_4')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_non_existing_key')

        assert self.config.get_boolean(
            'string_non_existing_key', is_optional=True) is None
        assert self.config.get_boolean(
            'string_non_existing_key', is_optional=True, default='foo') == 'foo'
