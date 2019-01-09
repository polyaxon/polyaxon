# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from hestia.user_path import polyaxon_user_path
from polyaxon_deploy.operators.cmd_operator import CmdOperator


class KubectlOperator(CmdOperator):
    CMD = 'kubectl'

    def params(self, args, is_json):
        params = [self.CMD] + args
        if is_json:
            params += ['-o', 'json']
        return params

    @staticmethod
    def env():
        env = os.environ.copy()
        env.update(dict(
            KUBECONFIG=env.get('KUBECONFIG', ''),
            PATH='{}:{}'.format(
                polyaxon_user_path(),
                env.get('PATH', ''),
            ).encode(),
        ))
        return env

    def execute(self, args, is_json=True):
        params = self.params(args, is_json=is_json)
        return self._execute(params=params, env=self.env(), is_json=is_json)
