# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import mock

from polyaxon_deploy.operators.exceptions import OperatorException
from polyaxon_deploy.operators.kubectl import KubectlOperator

DUMMY_RETURN_VALUE = object()


class TestKubectlOperator(TestCase):

    def setUp(self):
        self.kubectl = KubectlOperator()

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
    def test_kubectl(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, 'bar')
        assert self.kubectl.execute(['foo'], is_json=False) == 'bar'
        assert mock_subprocess.Popen.call_args[0][0] == ['kubectl', 'foo']

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_kubectl_json(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, '{"foo": "bar"}')
        assert self.kubectl.execute(['foo'], is_json=True) == dict(foo='bar')
        assert mock_subprocess.Popen.call_args[0][0] == ['kubectl', 'foo', '-o', 'json']

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_kubectl_error(self, mock_subprocess):
        return_code = 1
        stdout = "output"
        stderr = "error"
        mock_subprocess.Popen = self.mock_popen(return_code, stdout, stderr)
        with self.assertRaises(OperatorException) as exception:
            self.kubectl.execute(['foo'], is_json=False)

        self.assertEqual(
            exception.exception.message,
            "`kubectl` command ('kubectl', 'foo') "
            "failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                return_code,
                stdout,
                stderr)
        )
