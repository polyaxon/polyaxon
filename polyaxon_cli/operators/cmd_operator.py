# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import subprocess
import json

from tempfile import TemporaryFile

from polyaxon_cli.operators.exceptions import OperatorException


class CmdOperator(object):
    CMD = ''

    def _execute(self, params, env, is_json=False):
        with TemporaryFile('w+') as stdout, TemporaryFile('w+') as stderr:
            ps = subprocess.Popen(params, env=env, stdout=stdout, stderr=stderr)
            exit_status = ps.wait()
            stdout.seek(0)
            stderr.seek(0)
            if exit_status != 0:
                raise OperatorException(cmd=self.CMD,
                                        args=params,
                                        return_code=exit_status,
                                        stdout=stdout,
                                        stderr=stderr)

            if is_json:
                return json.load(stdout)
            else:
                return stdout.read()
