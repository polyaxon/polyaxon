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

from polyaxon.polyflow import V1Init, V1RunKind
from polyaxon.polyflow.operations import V1CompiledOperation
from tests.utils import BaseTestCase


@pytest.mark.init_mark
class TestInit(BaseTestCase):
    def test_op_with_init(self):
        config_dict = {
            "kind": "compiled_operation",
            "run": {
                "kind": V1RunKind.JOB,
                "container": {"image": "foo/bar"},
                "init": [
                    {"container": {"name": "init1", "args": ["/subpath1", "subpath2"]}},
                    {
                        "connection": "s3",
                        "container": {
                            "name": "init2",
                            "args": ["/subpath1", "subpath2"],
                        },
                    },
                    {"connection": "repo3", "git": {"revision": "foo"}},
                ],
            },
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_init_config(self):
        config_dict = {
            "container": {"name": "init1", "args": ["/subpath1", "subpath2"]}
        }
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {"connection": "foo"}
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "connection": "foo",
            "container": {"name": "init1", "args": ["/subpath1", "subpath2"]},
        }
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "connection": "foo",
            "git": {"revision": "branch1"},
            "container": {"name": "init1", "args": ["/subpath1", "subpath2"]},
        }
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "connection": "foo",
            "artifacts": {"files": ["path1", "path2"]},
            "container": {"name": "init1", "args": ["/subpath1", "subpath2"]},
        }
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "dockerfile": {
                "image": "tensorflow:1.3.0",
                "path": ["./module"],
                "copy": ["/foo/bar"],
                "run": ["pip install tensor2tensor"],
                "env": {"LC_ALL": "en_US.UTF-8"},
                "filename": "dockerfile",
                "workdir": "",
                "shell": "sh",
            }
        }
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        # artifacts without connection
        config_dict = {"artifacts": {"files": ["path1", "path2"]}}
        config = V1Init.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_wrong_init_configs(self):
        # Git without url and connection
        config_dict = {
            "git": {"revision": "branch1"},
            "container": {"name": "init1", "args": ["/subpath1", "subpath2"]},
        }
        with self.assertRaises(ValidationError):
            V1Init.from_dict(config_dict)

        # artifacts without connection
        config_dict = {
            "git": {"revision": "branch1"},
            "artifacts": {"files": ["path1", "path2"]},
        }
        with self.assertRaises(ValidationError):
            V1Init.from_dict(config_dict)

        # both git and dockerfile at the same time
        config_dict = {
            "git": {"revision": "branch1"},
            "dockerfile": {"image": "tensorflow:1.3.0"},
        }
        with self.assertRaises(ValidationError):
            V1Init.from_dict(config_dict)
