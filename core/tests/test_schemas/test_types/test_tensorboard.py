#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.schemas.types.tensorboard import V1TensorboardType
from polyaxon.utils.test_utils import BaseTestCase


@pytest.mark.init_mark
class TestTensorboardInitConfigs(BaseTestCase):
    def test_tb_type(self):
        config_dict = {
            "port": 6006,
            "uuids": [
                "d1410a914d18457589b91926d8c23db4",
                "56f1a7f20f1d4f7f9e1a108b3c6b6031",
            ],
            "useNames": True,
            "plugins": ["tensorboard-plugin-profile"],
        }
        config = V1TensorboardType.from_dict(config_dict)
        assert config.to_dict() == config_dict
