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

import pytest

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.docker import docker
from polyaxon.schemas.polyflow.init.build_context import BuildContextConfig


@pytest.mark.cli_mark
class TestCliDocker(BaseCommandTestCase):
    @patch("polyaxon.builds.generator.generator.DockerFileGenerator.create")
    def test_docker_build_context(self, generate_create):
        build_context = BuildContextConfig(image="foo")
        self.runner.invoke(
            docker,
            ["generate", "--build-context={}".format(build_context.to_dict(dump=True))],
        )
        assert generate_create.call_count == 1
