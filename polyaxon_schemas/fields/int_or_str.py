# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields


class IntOrStr(fields.Str):
    default_error_messages = {
        'invalid': 'Not a valid string or int.',
        'invalid_utf8': 'Not a valid utf-8 string.'
    }

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, int):
            return int(value)

        return super(IntOrStr, self)._serialize(value=value, attr=attr, obj=obj)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int):
            return int(value)

        return super(IntOrStr, self)._deserialize(value=value, attr=attr, data=data)
