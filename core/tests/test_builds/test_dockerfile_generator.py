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

import os
import tempfile

import pytest

from tests.utils import BaseTestCase

from polyaxon.builds.generator.generator import DockerFileGenerator
from polyaxon.schemas.types.dockerfile import (
    POLYAXON_DOCKER_WORKDIR,
    POLYAXON_DOCKERFILE_NAME,
    V1DockerfileType,
)


@pytest.mark.api_builds
class TestDockerfileGenerator(BaseTestCase):
    @staticmethod
    def touch(path):
        with open(path, "w") as f:
            f.write("test")

    def test_get_generated_dockerfile_path(self):
        # Create a repo folder
        repo_path = os.path.join(tempfile.mkdtemp(), "repo")
        os.mkdir(repo_path)
        build_context = V1DockerfileType(image="busybox")

        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )
        assert builder.dockerfile_path == "{}/{}".format(
            repo_path, POLYAXON_DOCKERFILE_NAME
        )
        builder.clean()

    def test_render_works_as_expected(self):  # pylint:disable=too-many-statements
        # Create a repo folder
        repo_path = os.path.join(tempfile.mkdtemp(), "repo")
        os.mkdir(repo_path)

        build_context = V1DockerfileType(image="busybox")

        # By default, it should use FROM image declare WORKDIR
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        builder.clean()

        assert "FROM busybox" in dockerfile
        assert "WORKDIR {}".format(POLYAXON_DOCKER_WORKDIR) in dockerfile
        assert "COPY" not in dockerfile

        # By default, it should use FROM image declare WORKDIR, and work
        build_context = V1DockerfileType(image="busybox", workdir_path=repo_path)
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        builder.clean()
        assert "COPY {}".format(repo_path) in dockerfile

        # No lang env
        assert "LC_ALL" not in dockerfile
        assert "LANG" not in dockerfile
        assert "LANGUAGE" not in dockerfile

        # Add env vars
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, env=[("BLA", "BLA")]
        )
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "ENV BLA BLA" in dockerfile
        assert "groupadd" not in dockerfile
        assert "useradd" not in dockerfile
        builder.clean()

        # Add copy steps
        copy = ["polyaxon_requirements.txt", "polyaxon_setup.sh", "environment.yml"]
        # Add run steps to act on them
        run = [
            "pip install -r polyaxon_requirements.txt",
            "./polyaxon_setup.sh",
            "conda env update -n base -f environment.yml",
        ]
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, copy=copy, run=run
        )

        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "COPY {} {}".format(copy[0], POLYAXON_DOCKER_WORKDIR) in dockerfile
        assert "COPY {} {}".format(copy[1], POLYAXON_DOCKER_WORKDIR) in dockerfile
        assert "COPY {} {}".format(copy[2], POLYAXON_DOCKER_WORKDIR) in dockerfile

        assert "RUN {}".format(run[0]) in dockerfile
        assert "RUN {}".format(run[1]) in dockerfile
        assert "RUN {}".format(run[2]) in dockerfile
        assert "groupadd" not in dockerfile
        assert "useradd" not in dockerfile
        builder.clean()

        # Add uid but no gid
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, uid=1000
        )

        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "groupadd" not in dockerfile
        assert "useradd" not in dockerfile
        assert "1000" not in dockerfile
        builder.clean()

        # Add gid but no uid
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, gid=1000
        )
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "groupadd" not in dockerfile
        assert "useradd" not in dockerfile
        assert "1000" not in dockerfile
        builder.clean()

        # Add uid and gid
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, uid=1000, gid=1000
        )
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "groupadd" in dockerfile
        assert "useradd" in dockerfile
        assert "-u 1000" in dockerfile
        assert "-g 1000" in dockerfile
        builder.clean()

        # Add lan env
        build_context = V1DockerfileType(
            image="busybox", workdir_path=repo_path, lang_env="en_US.UTF-8"
        )
        builder = DockerFileGenerator(
            build_context=build_context, destination=repo_path
        )

        dockerfile = builder.render()
        assert "en_US.UTF-8" in dockerfile
        assert "LC_ALL" in dockerfile
        assert "LANG" in dockerfile
        assert "LANGUAGE" in dockerfile
        builder.clean()


class TestGenerate(BaseTestCase):
    def test_generate(self):
        # Create a repo folder
        tmp_path = tempfile.mkdtemp()

        assert not os.path.isfile("{}/{}".format(tmp_path, POLYAXON_DOCKERFILE_NAME))

        build_context = V1DockerfileType(
            image="busybox",
            workdir_path=tmp_path,
            lang_env="en_US.UTF-8",
            uid=100,
            gid=100,
        )
        DockerFileGenerator(build_context=build_context, destination=tmp_path).create()
        assert os.path.isfile("{}/{}".format(tmp_path, POLYAXON_DOCKERFILE_NAME))
