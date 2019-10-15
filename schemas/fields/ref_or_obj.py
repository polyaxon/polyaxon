# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields
from marshmallow.base import FieldABC

from schemas.fields.params import PARAM_REGEX


def get_ref_or_obj(container, value):
    try:
        return container.deserialize(value)
    except (ValueError, TypeError, ValidationError):
        pass

    if not isinstance(value, six.string_types):
        raise ValidationError(
            "This field expects an {container} or a str containing a param reference.".format(
                container=container.__class__.__name__
            )
        )

    param = PARAM_REGEX.search(value)
    if not param:
        raise ValidationError(
            "This field expects an {container} or a param ref inside {{  }}.".format(
                container=container.__class__.__name__
            )
        )
    return value


class RefOrObject(fields.Field):
    def __init__(self, cls_or_instance, **kwargs):

        super(RefOrObject, self).__init__(allow_none=True, **kwargs)
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, FieldABC):
                raise ValueError(
                    "The type of the element "
                    "must be a subclass of "
                    "marshmallow.base.FieldABC"
                )
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, FieldABC):
                raise ValueError(
                    "The instances of the "
                    "element must be of type "
                    "marshmallow.base.FieldABC"
                )
            self.container = cls_or_instance

    def _validate(self, value):
        if isinstance(value, six.string_types):
            param = PARAM_REGEX.search(value)
            if not param:
                super(RefOrObject, self)._validate(value)
        else:
            super(RefOrObject, self)._validate(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return get_ref_or_obj(self.container, value)
