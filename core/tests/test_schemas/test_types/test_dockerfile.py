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

from polyaxon.schemas.types.dockerfile import (
    POLYAXON_DOCKER_SHELL,
    POLYAXON_DOCKER_WORKDIR,
    POLYAXON_DOCKERFILE_NAME,
    V1DockerfileType,
)
from tests.utils import BaseTestCase


@pytest.mark.init_mark
class TestDockerfileInitConfigs(BaseTestCase):
    def test_valid_image(self):
        config_dict = {"image": None}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": ""}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "some_image_name:sdf:sdf:foo"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "registry.foobar.com/my/docker/some_image_name:foo:foo"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "some_image_name / foo"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "some_image_name /foo:sdf"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "some_image_name /foo :sdf"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {
            "image": "registry.foobar.com:foo:foo/my/docker/some_image_name:foo"
        }
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "registry.foobar.com:foo:foo/my/docker/some_image_name"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

        config_dict = {"image": "registry.foobar.com:/my/docker/some_image_name:foo"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

    def test_does_not_accept_dockerfiles(self):
        config_dict = {"dockerfile": "foo/bar"}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)

    def test_build_config(self):
        config_dict = {"image": "some_image_name"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "latest"

    def test_build_config_image_use_cases(self):
        # Latest
        config_dict = {"image": "some_image_name"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "latest"

        # Latest from with docker registry url
        config_dict = {"image": "registry.foobar.com/my/docker/some_image_name"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "latest"

        # Latest from with docker registry url with port
        config_dict = {"image": "registry.foobar.com:4567/some_image_name"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "latest"

        # Some tag
        config_dict = {"image": "some_image_name:4567"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "4567"

        # Some tag
        config_dict = {"image": "some_image_name:foo"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "foo"

        # Some tag from with docker registry url
        config_dict = {"image": "registry.foobar.com/my/docker/some_image_name:foo"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "foo"

        # Some tag from with docker registry url with port
        config_dict = {"image": "registry.foobar.com:4567/some_image_name:foo"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "foo"

    def test_build_repo_with_install_step_copy_path_config(self):
        config_dict = {
            "image": "tensorflow:1.3.0",
            "path": ["./module"],
            "copy": ["/foo/bar"],
            "run": ["pip install tensor2tensor"],
            "env": {"LC_ALL": "en_US.UTF-8"},
            "filename": "dockerfile",
            "workdir": "",
            "shell": "sh",
        }
        config = V1DockerfileType.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.image_tag == "1.3.0"

    def test_build_repo_with_security_context(self):
        config_dict = {
            "image": "tensorflow:1.3.0",
            "run": ["pip install tensor2tensor"],
            "env": {"LC_ALL": "en_US.UTF-8"},
            "uid": 1000,
            "gid": 3000,
            "filename": "dockerfile",
            "workdir": "",
            "shell": "sh",
        }
        config = V1DockerfileType.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.image_tag == "1.3.0"
        assert config.uid == 1000
        assert config.gid == 3000

    def test_build_config_with_default_values(self):
        config_dict = {"image": "some_image_name"}
        config = V1DockerfileType.from_dict(config_dict)
        assert config.image_tag == "latest"
        assert config.filename == POLYAXON_DOCKERFILE_NAME
        assert config.shell == POLYAXON_DOCKER_SHELL
        assert config.workdir == POLYAXON_DOCKER_WORKDIR

        config_dict = {}
        with self.assertRaises(ValidationError):
            V1DockerfileType.from_dict(config_dict)
