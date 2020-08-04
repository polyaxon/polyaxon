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

import json
import subprocess

from tempfile import TemporaryFile

from polyaxon.exceptions import PolyaxonOperatorException


class CmdOperator:
    CMD = ""

    @classmethod
    def _execute(cls, params, env, is_json=False, stream=False):
        def _stream():
            with TemporaryFile("w+") as stderr:
                ps = subprocess.Popen(params, env=env, stderr=stderr)
                exit_status = ps.wait()
                stderr.seek(0)
                if exit_status != 0:
                    raise PolyaxonOperatorException(
                        cmd=cls.CMD,
                        args=params,
                        return_code=exit_status,
                        stdout=None,
                        stderr=stderr,
                    )

        def _block():
            with TemporaryFile("w+") as stdout, TemporaryFile("w+") as stderr:
                ps = subprocess.Popen(params, env=env, stdout=stdout, stderr=stderr)
                exit_status = ps.wait()
                stdout.seek(0)
                stderr.seek(0)
                if exit_status != 0:
                    raise PolyaxonOperatorException(
                        cmd=cls.CMD,
                        args=params,
                        return_code=exit_status,
                        stdout=stdout,
                        stderr=stderr,
                    )

                return json.load(stdout) if is_json else stdout.read()

        return _stream() if stream else _block()

    @classmethod
    def check(cls):
        return True
