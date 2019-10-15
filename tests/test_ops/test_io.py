# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from unittest import TestCase

import pytest

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from schemas.ops.io import IOConfig, IOTypes


@pytest.mark.ops_mark
class TestIOConfigs(TestCase):
    def test_wrong_io_config(self):
        # No name
        with self.assertRaises(TypeError):
            IOConfig.from_dict({})

    def test_unsupported_io_config_type(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict({"name": "input1", "type": "something"})

    def test_wrong_io_config_default(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict(
                {"name": "input1", "type": IOTypes.FLOAT, "value": "foo"}
            )

        with self.assertRaises(ValidationError):
            IOConfig.from_dict(
                {"name": "input1", "type": IOTypes.GCS_PATH, "value": 234}
            )

    def test_wrong_io_config_flag(self):
        with self.assertRaises(ValidationError):
            IOConfig.from_dict(
                {"name": "input1", "type": IOTypes.S3_PATH, "is_flag": True}
            )

        with self.assertRaises(ValidationError):
            IOConfig.from_dict(
                {"name": "input1", "type": IOTypes.FLOAT, "is_flag": True}
            )

    def test_io_config_optionals(self):
        config_dict = {"name": "input1"}
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_desc(self):
        # test desc
        config_dict = {"name": "input1", "description": "some text"}
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_io_config_types(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.INT,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(name="input1", type="int", value=3)
        assert config.get_repr_from_value(3) == expected_repr
        assert config.get_repr() == OrderedDict(name="input1", type="int")

        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.S3_PATH,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(
            name="input1", type=IOTypes.S3_PATH, value="s3://foo"
        )
        assert config.get_repr_from_value("s3://foo") == expected_repr
        assert config.get_repr() == OrderedDict(name="input1", type=IOTypes.S3_PATH)

    def test_io_config_default(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.BOOL,
            "is_optional": True,
            "value": True,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(name="input1", type="bool", value=True)
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr

        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.FLOAT,
            "is_optional": True,
            "value": 3.4,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(name="input1", type="float", value=3.4)
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr

    def test_io_config_default_and_required(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.BOOL,
            "value": True,
            "is_optional": True,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.STR,
            "value": "foo",
        }
        with self.assertRaises(ValidationError):
            IOConfig.from_dict(config_dict)

    def test_io_config_required(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": "float",
            "is_optional": False,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(name="input1", type="float", value=1.1)
        assert config.get_repr_from_value(1.1) == expected_repr
        assert config.get_repr() == OrderedDict(name="input1", type="float")

    def test_io_config_flag(self):
        config_dict = {
            "name": "input1",
            "description": "some text",
            "type": IOTypes.BOOL,
            "is_flag": True,
        }
        config = IOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
        expected_repr = OrderedDict(name="input1", type="bool", value=False)
        assert config.get_repr_from_value(False) == expected_repr

    def test_value_non_typed_input(self):
        config_dict = {"name": "input1"}
        config = IOConfig.from_dict(config_dict)
        assert config.validate_value("foo") == "foo"
        assert config.validate_value(1) == 1
        assert config.validate_value(True) is True

        expected_repr = OrderedDict(name="input1", value="foo")
        assert config.get_repr_from_value("foo") == expected_repr
        assert config.get_repr() == OrderedDict(name="input1")

    def test_value_typed_input(self):
        config_dict = {"name": "input1", "type": IOTypes.BOOL}
        config = IOConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value("foo")
        with self.assertRaises(ValidationError):
            config.validate_value(1)
        with self.assertRaises(ValidationError):
            config.validate_value(None)

        assert config.validate_value(True) is True

    def test_value_typed_input_with_default(self):
        config_dict = {
            "name": "input1",
            "type": IOTypes.INT,
            "value": 12,
            "is_optional": True,
        }
        config = IOConfig.from_dict(config_dict)
        with self.assertRaises(ValidationError):
            config.validate_value("foo")

        assert config.validate_value(1) == 1
        assert config.validate_value(0) == 0
        assert config.validate_value(-1) == -1
        assert config.validate_value(None) == 12
        expected_repr = OrderedDict(name="input1", type="int", value=12)
        assert config.get_repr_from_value(None) == expected_repr
        assert config.get_repr() == expected_repr
