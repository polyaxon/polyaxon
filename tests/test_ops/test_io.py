# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.io import IOTypes
from polyaxon_schemas.ops.io.io import IOConfig


class TestIOConfigs(TestCase):
    def test_wrong_io_config(self):
        # No name
        with self.assertRaises(TypeError):
            IOConfig.from_dict({})

    def test_unsupported_io_config_type(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict({
                'name': 'input1',
                'type': 'something'
            })

    def test_wrong_io_config_default(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict({
                'name': 'input1',
                'type': IOTypes.FLOAT,
                'default': 'foo'
            })

        with self.assertRaises(ValidationError):
            IOConfig.from_dict({
                'name': 'input1',
                'type': IOTypes.GCS_PATH,
                'default': 234
            })

    def test_wrong_io_config_flag(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict({
                'name': 'input1',
                'type': IOTypes.S3_PATH,
                'is_flag': True
            })

        with self.assertRaises(ValidationError):
            IOConfig.from_dict({
                'name': 'input1',
                'type': IOTypes.FLOAT,
                'is_flag': True
            })

    def test_io_config_optionals(self):
        config_dict = {
            'name': 'input1',
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_desc(self):
        # test desc
        config_dict = {
            'name': 'input1',
            'description': 'some text'
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_types(self):
        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.INT
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.S3_PATH
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_default(self):
        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.BOOL,
            'is_optional': True,
            'default': True,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.FLOAT,
            'is_optional': True,
            'default': 3.4,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_default_and_required(self):
        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.BOOL,
            'default': True,
            'is_optional': True
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.STR,
            'default': 'foo'
        }
        with self.assertRaises(ValidationError):
            IOConfig.from_dict(config_dict)

    def test_io_config_required(self):
        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': 'float',
            'is_optional': False,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_flag(self):
        config_dict = {
            'name': 'input1',
            'description': 'some text',
            'type': IOTypes.BOOL,
            'is_flag': True,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_value_non_typed_input(self):
        config_dict = {
            'name': 'input1'
        }
        config = IOConfig.from_dict(config_dict)
        assert config.validate_value('foo') == 'foo'
        assert config.validate_value(1) == 1
        assert config.validate_value(True) is True

    def test_value_typed_input(self):
        config_dict = {
            'name': 'input1',
            'type': IOTypes.BOOL
        }
        config = IOConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value('foo')
        with self.assertRaises(ValidationError):
            config.validate_value(1)
        with self.assertRaises(ValidationError):
            config.validate_value(None)

        assert config.validate_value(True) is True

    def test_value_typed_input_with_default(self):
        config_dict = {
            'name': 'input1',
            'type': IOTypes.INT,
            'default': 12,
            'is_optional': True,
        }
        config = IOConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value('foo')

        assert config.validate_value(1) == 1
        assert config.validate_value(0) == 0
        assert config.validate_value(-1) == -1
        assert config.validate_value(None) == 12
