import os

import pytest

from config_manager.config_manager import ConfigManager
from config_manager.exceptions import ConfigurationError
from polyaxon.config_manager import SettingsConfigManager
from tests.utils import BaseTest


@pytest.mark.config_manager_mark
class TestConfigManager(BaseTest):
    def setUp(self):
        os.environ['FOO_BAR_KEY'] = 'foo_bar'
        self.config = ConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/config_tests.json'])

    def test_get_from_os_env(self):
        assert self.config.get_string('FOO_BAR_KEY') == 'foo_bar'

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

        value = self.config.get_boolean('bool_list_key_1', is_list=True)
        self.assertEqual(value, [False, False, True, True, True, False])

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
            self.config.get_boolean('bool_list_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_list_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_list_error_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_non_existing_key', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_boolean('bool_key_2', is_list=True)

        self.assertEqual(self.config.get_boolean('bool_non_existing_key', is_optional=True), None)
        self.assertEqual(self.config.get_boolean(
            'bool_non_existing_key', is_optional=True, default=True), True)

        self.assertEqual(self.config.get_boolean(
            'bool_non_existing_key', is_list=True, is_optional=True), None)
        self.assertEqual(self.config.get_boolean(
            'bool_non_existing_key', is_list=True, is_optional=True, default=[True, False]),
            [True, False])

    def test_get_int(self):
        value = self.config.get_int('int_key_1')
        self.assertEqual(value, 123)

        value = self.config.get_int('int_key_2')
        self.assertEqual(value, 123)

        value = self.config.get_int('int_list_key_1', is_list=True)
        self.assertEqual(value, [123, 124, 125, 125])

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_list_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_list_error_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_list_error_key_2', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_list_error_key_3', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_key_2', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_int('int_non_existing_key')

        self.assertEqual(self.config.get_int(
            'int_non_existing_key', is_optional=True), None)
        self.assertEqual(self.config.get_int(
            'int_non_existing_key', is_optional=True, default=34), 34)

        self.assertEqual(self.config.get_int(
            'int_non_existing_key', is_list=True, is_optional=True), None)
        self.assertEqual(self.config.get_int(
            'int_non_existing_key', is_list=True, is_optional=True, default=[34, 1]), [34, 1])

    def test_get_float(self):
        value = self.config.get_float('float_key_1')
        self.assertEqual(value, 1.23)

        value = self.config.get_float('float_key_2')
        self.assertEqual(value, 1.23)

        value = self.config.get_float('float_key_3')
        self.assertEqual(value, 123)

        value = self.config.get_float('float_list_key_1', is_list=True)
        self.assertEqual(value, [1.23, 13.3, 4.4, 555., 66.])

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_error_key_4')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_list_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_list_error_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_list_error_key_2', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_list_error_key_3', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_key_2', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_float('float_non_existing_key')

        self.assertEqual(self.config.get_float(
            'float_non_existing_key', is_optional=True), None)
        self.assertEqual(self.config.get_float(
            'float_non_existing_key', is_optional=True, default=3.4), 3.4)

        self.assertEqual(self.config.get_float(
            'float_non_existing_key', is_list=True, is_optional=True), None)
        self.assertEqual(self.config.get_float(
            'float_non_existing_key', is_list=True, is_optional=True, default=[3.4, 1.2]),
            [3.4, 1.2])

    def test_get_string(self):
        value = self.config.get_string('string_key_1')
        self.assertEqual(value, "123")

        value = self.config.get_string('string_key_2')
        self.assertEqual(value, "1.23")

        value = self.config.get_string('string_key_3')
        self.assertEqual(value, "foo")

        value = self.config.get_string('string_key_4')
        self.assertEqual(value, "")

        value = self.config.get_string('string_list_key_1', is_list=True)
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_2')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_3')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_error_key_4')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_list_key_1')

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_list_error_key_1', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_list_error_key_2', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_list_error_key_3', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_list_error_key_4', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_key_3', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_key_4', is_list=True)

        with self.assertRaises(ConfigurationError):
            self.config.get_string('string_non_existing_key')

        self.assertEqual(self.config.get_string(
            'string_non_existing_key', is_optional=True), None)
        self.assertEqual(self.config.get_string(
            'string_non_existing_key', is_optional=True, default='foo'), 'foo')

        self.assertEqual(self.config.get_string(
            'string_non_existing_key', is_list=True, is_optional=True), None)
        self.assertEqual(self.config.get_string(
            'string_non_existing_key', is_list=True, is_optional=True, default=['foo', 'bar']),
            ['foo', 'bar'])


@pytest.mark.config_manager_mark
class TestSettingsConfigManager(BaseTest):
    def test_get_from_os_env(self):
        os.environ['POLYAXON_ENVIRONMENT'] = 'testing'
        os.environ['FOO_BAR_KEY'] = 'foo_bar'
        config = SettingsConfigManager.read_configs(
            [os.environ,
             './tests/fixtures_static/configs/config_tests.json',
             './tests/fixtures_static/configs/non_opt_config_tests.json'])

        assert config.get_string('POLYAXON_ENVIRONMENT') == 'testing'
        assert config.get_string('FOO_BAR_KEY') == 'foo_bar'

    def test_raises_for_non_optional_env_vars(self):
        with self.assertRaises(ConfigurationError):
            SettingsConfigManager.read_configs(
                [os.environ,
                 './tests/fixtures_static/configs/config_tests.json'])
