# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from hestia.user_path import polyaxon_user_path
from polyaxon_deploy.operators.cmd_operator import CmdOperator


class KubectlOperator(CmdOperator):
    CMD = 'kubectl'

    @classmethod
    def params(cls, args, is_json):
        params = [cls.CMD] + args
        if is_json:
            params += ['-o', 'json']
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=[], is_json=False)
        if not command_exist:
            return False
        command_exist = cls.execute(args=['version'])
        if not command_exist:
            return False
        return True

    @staticmethod
    def env():
        env = os.environ.copy()
        env.update(dict(
            KUBECONFIG=env.get('KUBECONFIG', ''),
            PATH='{}:{}'.format(
                polyaxon_user_path(),
                env.get('PATH', ''),
            ),
        ))
        return env

    @classmethod
    def execute(cls, args, is_json=True, stream=False):
        params = cls.params(args, is_json=is_json)
        return cls._execute(params=params, env=cls.env(), is_json=is_json, stream=stream)
