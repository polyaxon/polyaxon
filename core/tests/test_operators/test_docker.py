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

from tests.utils import BaseTestCase

from polyaxon.deploy.operators.docker import DockerOperator
from polyaxon.exceptions import PolyaxonOperatorException

DUMMY_RETURN_VALUE = object()


@pytest.mark.operators_mark
class TestDockerOperator(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.docker = DockerOperator()

    @staticmethod
    def mock_popen(return_code, out_msg, err_msg=None):
        def popen(*args, **kwargs):
            stdout = kwargs.pop("stdout")
            stdout.write(out_msg)
            if err_msg:
                stderr = kwargs.pop("stderr")
                stderr.write(err_msg)
            return mock.Mock(wait=mock.Mock(return_value=return_code))

        return mock.Mock(side_effect=popen)

    @mock.patch("polyaxon.deploy.operators.cmd_operator.subprocess")
    def test_docker(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, "bar")
        assert self.docker.execute(["volume"]) == "bar"
        assert mock_subprocess.Popen.call_args[0][0] == ["docker", "volume"]

    @mock.patch("polyaxon.deploy.operators.cmd_operator.subprocess")
    def test_docker_set_volume(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, "bar")
        assert self.docker.set_volume("foo") == "bar"
        assert mock_subprocess.Popen.call_args[0][0] == [
            "docker",
            "volume",
            "create",
            "--name=foo",
        ]

    @mock.patch("polyaxon.deploy.operators.cmd_operator.subprocess")
    def test_docker_error(self, mock_subprocess):
        return_code = 1
        stdout = "output"
        stderr = "error"
        mock_subprocess.Popen = self.mock_popen(return_code, stdout, stderr)
        with self.assertRaises(PolyaxonOperatorException) as exception:
            self.docker.execute(["run"])

        self.assertEqual(
            exception.exception.message,
            "`docker` command ('docker', 'run') "
            "failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                return_code, stdout, stderr
            ),
        )
