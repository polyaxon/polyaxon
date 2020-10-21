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

import mock
import pytest

from urllib3.exceptions import ReadTimeoutError

from polyaxon.builds.builder import DockerBuilder, DockerPusher, build, build_and_push
from polyaxon.exceptions import PolyaxonBuildException
from polyaxon.schemas.types import V1UriType
from tests.utils import BaseTestCase


@pytest.mark.api_builds
class TestDockerBuilder(BaseTestCase):
    @staticmethod
    def touch(path):
        with open(path, "w") as f:
            f.write("test")

    @mock.patch("docker.APIClient.images")
    def test_check_image(self, check_image):
        builder = DockerBuilder(context=".", destination="image:tag")
        builder.check_image()
        assert check_image.call_count == 1
        assert check_image.call_args[0] == ("image:tag",)

    def test_validate_registries(self):
        with self.assertRaises(PolyaxonBuildException):
            DockerBuilder(context=".", destination="image:tag", registries="foo")

        with self.assertRaises(PolyaxonBuildException):
            DockerBuilder(
                context=".",
                destination="image:tag",
                registries=["foo", V1UriType("user", "pwd", "host")],
            )

        builder = DockerBuilder(
            context=".",
            destination="image:tag",
            registries=[V1UriType("user", "pwd", "host")],
        )

        assert builder.registries is not None

    @mock.patch("docker.APIClient.login")
    def test_login_registries(self, login_mock):
        builder = DockerBuilder(
            context=".",
            destination="image:tag",
            registries=[
                V1UriType("user", "pwd", "host"),
                V1UriType("user", "pwd", "host"),
            ],
        )
        builder.login_private_registries()
        assert login_mock.call_count == 2

    @mock.patch("docker.APIClient.build")
    def test_build(self, build_mock):
        builder = DockerBuilder(context=".", destination="image:tag")
        builder.build()
        assert build_mock.call_count == 1

    @mock.patch("docker.APIClient.push")
    def test_push(self, push_mock):
        builder = DockerPusher(destination="image:tag")
        builder.push()
        assert push_mock.call_count == 1


class TestBuilder(BaseTestCase):
    @mock.patch("docker.APIClient.build")
    @mock.patch("docker.APIClient.login")
    def test_build_no_login(self, login_mock, build_mock):
        build(
            context=".",
            destination="image_name:image_tag",
            nocache=True,
            registries=None,
        )
        assert login_mock.call_count == 0
        assert build_mock.call_count == 1

    @mock.patch("docker.APIClient.build")
    @mock.patch("docker.APIClient.login")
    def test_build_login(self, login_mock, build_mock):
        build(
            context=".",
            destination="image_name:image_tag",
            nocache=True,
            registries=[
                V1UriType("user", "pwd", "host"),
                V1UriType("user", "pwd", "host"),
            ],
        )
        assert login_mock.call_count == 2
        assert build_mock.call_count == 1

    @mock.patch("docker.APIClient.push")
    @mock.patch("docker.APIClient.build")
    @mock.patch("docker.APIClient.login")
    def test_build_and_push(self, login_mock, build_mock, push_mock):
        build_and_push(
            context=".",
            destination="image_name:image_tag",
            nocache=True,
            registries=[
                V1UriType("user", "pwd", "host"),
                V1UriType("user", "pwd", "host"),
            ],
        )
        assert login_mock.call_count == 2
        assert build_mock.call_count == 1
        assert push_mock.call_count == 1

    @mock.patch("docker.APIClient.build")
    def test_build_raise_timeout(self, build_mock):
        build_mock.side_effect = ReadTimeoutError(None, "foo", "error")
        with self.assertRaises(PolyaxonBuildException):
            build(
                context=".",
                destination="image_name:image_tag",
                nocache=True,
                max_retries=1,
                sleep_interval=0,
            )

    @mock.patch("docker.APIClient.push")
    @mock.patch("docker.APIClient.build")
    def test_push_raise_timeout(self, build_mock, push_mock):
        push_mock.side_effect = ReadTimeoutError(None, "foo", "error")
        with self.assertRaises(PolyaxonBuildException):
            build_and_push(
                context=".",
                destination="image_name:image_tag",
                nocache=True,
                max_retries=1,
                sleep_interval=0,
            )
        assert build_mock.call_count == 1
