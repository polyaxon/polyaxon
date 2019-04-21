# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_deploy.operators.cmd_operator import CmdOperator
from polyaxon_deploy.operators.exceptions import OperatorException


class DockerOperator(CmdOperator):
    CMD = 'docker'

    @classmethod
    def params(cls, args):
        params = [cls.CMD] + args
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=['version'])
        if not command_exist:
            return False
        return True

    @classmethod
    def execute(cls, args, stream=False):
        params = cls.params(args)
        return cls._execute(params=params, env=None, stream=stream)

    @classmethod
    def set_volume(cls, volume):
        args = ['volume', 'create', '--name={}'.format(volume)]
        if not volume:
            raise OperatorException('docker',
                                    args,
                                    None,
                                    None,
                                    'Volume name was not provided')
        return cls.execute(args)
