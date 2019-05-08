# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields


class Tensor(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, six.string_types):
            return [value, 0, 0]
        if isinstance(value, list) and len(value) == 3:
            condition = (isinstance(value[0], str) and
                         isinstance(value[1], int) and
                         isinstance(value[1], int))
            if condition:
                return value
        raise ValidationError("This field expects a str or a list of [str, int, int].")
