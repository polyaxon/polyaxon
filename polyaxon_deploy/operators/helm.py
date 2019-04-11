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
    def execute(cls, args):
        params = cls.params(args)
        return cls._execute(params=params, env=None)
