# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import mock

from polyaxon_deploy.operators.conda import CondaOperator
from polyaxon_deploy.operators.exceptions import OperatorException

DUMMY_RETURN_VALUE = object()


class TestCondaOperator(TestCase):

    def setUp(self):
        self.conda = CondaOperator()

    @staticmethod
    def mock_popen(return_code, out_msg, err_msg=None):
        def popen(*args, **kwargs):
            stdout = kwargs.pop('stdout')
            stdout.write(out_msg)
            if err_msg:
                stderr = kwargs.pop('stderr')
                stderr.write(err_msg)
            return mock.Mock(wait=mock.Mock(return_value=return_code))

        return mock.Mock(side_effect=popen)

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_conda(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, 'bar')
        assert self.conda.execute(['install']) == 'bar'
        assert mock_subprocess.Popen.call_args[0][0] == ['conda', 'install']

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_conda_json(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, '{"foo": "bar"}')
        assert self.conda.execute(['env', 'list', '--json'], is_json=True) == dict(foo='bar')
        assert mock_subprocess.Popen.call_args[0][0] == ['conda', 'env', 'list', '--json']

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_conda_error(self, mock_subprocess):
        return_code = 1
        stdout = "output"
        stderr = "error"
        mock_subprocess.Popen = self.mock_popen(return_code, stdout, stderr)
        with self.assertRaises(OperatorException) as exception:
            self.conda.execute(['run'])

        self.assertEqual(
            exception.exception.message,
            "`conda` command ('conda', 'run') "
            "failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                return_code,
                stdout,
                stderr)
        )
