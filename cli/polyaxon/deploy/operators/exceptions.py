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


class OperatorException(Exception):
    def __init__(self, cmd, args, return_code, stdout, stderr):
        self.cmd = cmd
        self.args = args
        self.return_code = return_code
        self.stdout = stdout.read() if stdout else None
        self.stderr = stderr.read()
        if stdout:
            self.message = "`{}` command {} failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                self.cmd, self.args, self.return_code, self.stdout, self.stderr
            )
        else:
            self.message = "`{}` command {} failed with exit status {}\nstderr:\n{}".format(
                self.cmd, self.args, self.return_code, self.stderr
            )
        super(OperatorException, self).__init__()

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
