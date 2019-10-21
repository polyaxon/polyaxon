# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError

from polyaxon.schemas.fields.docker_image import validate_image


@pytest.mark.ops_mark
class TestImageValidation(TestCase):
    def test_valid_image(self):
        assert validate_image(None) is None
        assert validate_image("") is None

        with self.assertRaises(ValidationError):
            validate_image("some_image_name:sdf:sdf:foo")

        with self.assertRaises(ValidationError):
            validate_image("registry.foobar.com/my/docker/some_image_name:foo:foo")

        with self.assertRaises(ValidationError):
            validate_image("some_image_name / foo")

        with self.assertRaises(ValidationError):
            validate_image("some_image_name /foo:sdf")

        with self.assertRaises(ValidationError):
            validate_image("some_image_name /foo :sdf")

        with self.assertRaises(ValidationError):
            validate_image("registry.foobar.com:foo:foo/my/docker/some_image_name:foo")

        with self.assertRaises(ValidationError):
            validate_image("registry.foobar.com:foo:foo/my/docker/some_image_name")

        with self.assertRaises(ValidationError):
            validate_image("registry.foobar.com:/my/docker/some_image_name:foo")
