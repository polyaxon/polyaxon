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

from polyaxon.deploy import reader
from polyaxon.deploy.operators.compose import ComposeOperator
from polyaxon.exceptions import PolyaxonOperatorException
from tests.utils import BaseTestCase

DUMMY_RETURN_VALUE = object()


@pytest.mark.operators_mark
class TestComposeOperator(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.compose = ComposeOperator()

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
    def test_docker_compose(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, "bar")
        assert self.compose.execute(["up"]) == "bar"
        assert mock_subprocess.Popen.call_args[0][0] == ["docker-compose", "up"]

    @mock.patch("polyaxon.deploy.operators.cmd_operator.subprocess")
    def test_docker_error(self, mock_subprocess):
        return_code = 1
        stdout = "output"
        stderr = "error"
        mock_subprocess.Popen = self.mock_popen(return_code, stdout, stderr)
        with self.assertRaises(PolyaxonOperatorException) as exception:
            self.compose.execute(["down"])

        self.assertEqual(
            exception.exception.message,
            "`docker-compose` command ('docker-compose', 'down') "
            "failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                return_code, stdout, stderr
            ),
        )

    def test_generate(self):
        config = reader.read("tests/fixtures/deployment/all_platform_values.yml")
        assert ComposeOperator.generate_env(config) is not None
