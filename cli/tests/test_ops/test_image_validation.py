#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
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
