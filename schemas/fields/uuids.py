# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields


class UUID(fields.UUID):
    """A UUID field."""

    def _serialize(self, value, attr, obj, **kwargs):
        validated = str(self._validated(value).hex) if value is not None else None
        return super(fields.String, self)._serialize(validated, attr, obj)  # noqa
