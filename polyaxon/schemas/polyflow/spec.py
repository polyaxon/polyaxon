# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import namedtuple


class DagOpSpec(namedtuple("DagOpSpec", "op upstream downstream")):
    def items(self):
        return self._asdict().items()

    def set_op(self, op):
        return self._replace(op=op)
