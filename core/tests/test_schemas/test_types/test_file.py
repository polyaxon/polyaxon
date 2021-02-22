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

from polyaxon.schemas.types.file import V1FileType
from tests.utils import BaseTestCase


@pytest.mark.init_mark
class TestFileInitConfigs(BaseTestCase):
    def test_file_type(self):
        config_dict = {
            "filename": "script.py",
            "kind": "file",
            "chmod": "+x",
            "content": "test",
        }
        config = V1FileType.from_dict(config_dict)
        assert config.to_dict() == config_dict
