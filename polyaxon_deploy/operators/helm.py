# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_deploy.operators.cmd_operator import CmdOperator


class HelmOperator(CmdOperator):
    CMD = 'helm'

    def params(self, args):
        params = [self.CMD] + args
        return params

    def execute(self, args):
        params = self.params(args)
        return self._execute(params=params, env=None)
