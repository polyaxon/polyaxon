# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import subprocess

from tempfile import TemporaryFile

from polyaxon_deploy.operators.exceptions import OperatorException


class CmdOperator(object):
    CMD = ''

    @classmethod
    def _execute(cls, params, env, is_json=False, stream=False):
        def _stream():
            with TemporaryFile('w+') as stderr:
                ps = subprocess.Popen(params, env=env, stderr=stderr)
                exit_status = ps.wait()
                stderr.seek(0)
                if exit_status != 0:
                    raise OperatorException(cmd=cls.CMD,
                                            args=params,
                                            return_code=exit_status,
                                            stdout=None,
                                            stderr=stderr)

        def _block():
            with TemporaryFile('w+') as stdout, TemporaryFile('w+') as stderr:
                ps = subprocess.Popen(params, env=env, stdout=stdout, stderr=stderr)
                exit_status = ps.wait()
                stdout.seek(0)
                stderr.seek(0)
                if exit_status != 0:
                    raise OperatorException(cmd=cls.CMD,
                                            args=params,
                                            return_code=exit_status,
                                            stdout=stdout,
                                            stderr=stderr)

                return json.load(stdout) if is_json else stdout.read()

        return _stream() if stream else _block()

    @classmethod
    def check(cls):
        return True
