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

import pytest

from marshmallow import ValidationError

from polyaxon.connections.schemas import V1K8sResourceSchema
from polyaxon.schemas.types import V1K8sResourceType
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.parser_mark
class TestV1K8sResourceType(BaseTestCase):
    def setUp(self):
        self.spec1 = V1K8sResourceType(name="test1", is_requested=True)
        self.spec2 = V1K8sResourceType(
            name="test2", schema=V1K8sResourceSchema(name="ref2"), is_requested=False
        )
        self.spec3 = V1K8sResourceType(
            name="test3",
            schema=V1K8sResourceSchema(
                name="ref3", items=["item45"], mount_path="/some_path"
            ),
            is_requested=False,
        )
        super().setUp()

    def test_from_model(self):
        result = V1K8sResourceType.from_model(self.spec1)
        assert result.is_requested is False
        result = V1K8sResourceType.from_model(self.spec2)
        assert result == self.spec2
        result = V1K8sResourceType.from_model(self.spec3)
        assert result == self.spec3

    def test_resource_config(self):
        config_dict = {"name": "foo"}
        config = V1K8sResourceSchema.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "mount_path": 213}
        with self.assertRaises(ValidationError):
            V1K8sResourceSchema.from_dict(config_dict)

        config_dict = {"name": "foo", "items": 213}
        with self.assertRaises(ValidationError):
            V1K8sResourceSchema.from_dict(config_dict)

        config_dict = {
            "name": "foo",
            "mountPath": "/foo/path",
            "items": ["item1", "item2"],
        }
        config = V1K8sResourceSchema.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "items": ["item1", "item2"]}
        config = V1K8sResourceSchema.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
