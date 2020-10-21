#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from polyaxon.polyflow.mounts import V1ArtifactsMount
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.mounts_mark
class TestArtifactConfigs(BaseTestCase):
    def test_artifact_config(self):
        config_dict = {"name": "foo"}
        config = V1ArtifactsMount.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "managed": 213}
        with self.assertRaises(ValidationError):
            V1ArtifactsMount.from_dict(config_dict)

        config_dict = {"name": "foo", "paths": ["item1", "item2"]}
        config = V1ArtifactsMount.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"name": "foo", "paths": ["item1", "item2"]}
        config = V1ArtifactsMount.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
