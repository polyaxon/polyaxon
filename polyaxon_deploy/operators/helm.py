# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_deploy.operators.cmd_operator import CmdOperator


class HelmOperator(CmdOperator):
    CMD = 'helm'

    @classmethod
    def params(cls, args):
        params = [cls.CMD] + args
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=[])
        if not command_exist:
            return False
        command_exist = cls.execute(args=['version'])
        if not command_exist:
            return False
        return True

    @classmethod
    def execute(cls, args, stream=False):
        params = cls.params(args)
        return cls._execute(params=params, env=None, stream=stream)
