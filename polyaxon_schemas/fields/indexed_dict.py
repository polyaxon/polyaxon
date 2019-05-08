# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from marshmallow import fields


class IndexedDict(fields.Dict):
    def _validated(self, value):
        """Check the dict has an index or raise a :exc:`ValidationError` if an error occurs."""
        if not (isinstance(value, Mapping) or 'index' in value):
            self.fail('invalid')
