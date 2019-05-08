# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields


class FloatOrStr(fields.Str):
    default_error_messages = {
        'invalid': 'Not a valid string or float.',
        'invalid_utf8': 'Not a valid utf-8 string.'
    }

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, (float, int)):
            return float(value)

        return super(FloatOrStr, self)._serialize(value=value, attr=attr, obj=obj)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (float, int)):
            return float(value)

        return super(FloatOrStr, self)._deserialize(value=value, attr=attr, data=data)
