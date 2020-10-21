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

from polyaxon.polyflow import V1RunKind
from polyaxon.polyflow.operations import V1CompiledOperation
from tests.utils import BaseTestCase


@pytest.mark.sidecars_mark
class TestSidecars(BaseTestCase):
    def test_sidecars_config(self):
        config_dict = {
            "kind": "compiled_operation",
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "foo/bar"},
                "sidecars": [
                    {"name": "sidecar1", "args": ["/subpath1", "subpath2"]},
                    {"name": "sidecar2", "args": ["/subpath1", "subpath2"]},
                ],
            },
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
