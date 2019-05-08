# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields


class StrOrFct(fields.Str):
    def serialize(self, attr, obj, accessor=None, **kwargs):
        value = getattr(obj, attr)
        if hasattr(value, '__call__') and hasattr(value, '__name__'):
            return value.__name__

        return super(StrOrFct, self).serialize(attr, obj, accessor)
