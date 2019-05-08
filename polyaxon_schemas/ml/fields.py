# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields


class DType(fields.Str):
    def serialize(self, attr, obj, accessor=None, **kwargs):
        value = getattr(obj, attr)
        if hasattr(value, 'name'):
            return value.name

        return super(DType, self).serialize(attr, obj, accessor)
