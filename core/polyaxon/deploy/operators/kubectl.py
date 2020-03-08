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

import os

from polyaxon.containers.contexts import CONTEXT_USER_POLYAXON_PATH
from polyaxon.deploy.operators.cmd_operator import CmdOperator


class KubectlOperator(CmdOperator):
    CMD = "kubectl"

    @classmethod
    def params(cls, args, is_json):
        params = [cls.CMD] + args
        if is_json:
            params += ["-o", "json"]
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=[], is_json=False)
        if not command_exist:
            return False
        command_exist = cls.execute(args=["version"])
        if not command_exist:
            return False
        return True

    @staticmethod
    def env():
        env = os.environ.copy()
        env.update(
            dict(
                KUBECONFIG=env.get("KUBECONFIG", ""),
                PATH="{}:{}".format(CONTEXT_USER_POLYAXON_PATH, env.get("PATH", "")),
            )
        )
        return env

    @classmethod
    def execute(cls, args, is_json=True, stream=False):
        params = cls.params(args, is_json=is_json)
        return cls._execute(
            params=params, env=cls.env(), is_json=is_json, stream=stream
        )
