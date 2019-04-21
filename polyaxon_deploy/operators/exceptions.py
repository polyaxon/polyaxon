# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class OperatorException(Exception):
    def __init__(self, cmd, args, return_code, stdout, stderr):
        self.cmd = cmd
        self.args = args
        self.return_code = return_code
        self.stdout = stdout.read() if stdout else None
        self.stderr = stderr.read()
        if stdout:
            self.message = (
                '`{}` command {} failed with exit status {}\nstdout:\n{}\nstderr:\n{}'.format(
                    self.cmd,
                    self.args,
                    self.return_code,
                    self.stdout,
                    self.stderr,
                ))
        else:
            self.message = (
                '`{}` command {} failed with exit status {}\nstderr:\n{}'.format(
                    self.cmd,
                    self.args,
                    self.return_code,
                    self.stderr,
                ))
        super(OperatorException, self).__init__()

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
