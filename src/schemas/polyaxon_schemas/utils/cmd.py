#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import shlex

from subprocess import PIPE

from psutil import Popen


def run_command(cmd, data, location, chw, env=None):
    cmd_env = None
    if env:
        cmd_env = os.environ.copy()
        cmd_env.update(env)
    cwd = os.getcwd()
    if location is not None and chw is True:
        cwd = location
    elif location is not None and chw is False:
        cmd = "{0} {1}".format(cmd, location)
    r = Popen(
        shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd, env=cmd_env
    )
    if data is None:
        output = r.communicate()[0].decode("utf-8")
    else:
        output = r.communicate(input=data)[0]
    return output
