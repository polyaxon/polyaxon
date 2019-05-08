# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from marshmallow import fields


class DictOrStr(fields.Str):
    default_error_messages = {
        'invalid': 'Not a valid string or dict.',
        'invalid_utf8': 'Not a valid utf-8 string.'
    }

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, Mapping):
            return value

        return super(DictOrStr, self)._serialize(value=value, attr=attr, obj=obj)

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, Mapping):
            return value

        return super(DictOrStr, self)._deserialize(value=value, attr=attr, data=data)
