# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate
from marshmallow.base import FieldABC


def get_obj_or_list_obj(container, value, min_length=None, max_length=None):
    try:
        return container.deserialize(value)
    except (ValueError, TypeError, ValidationError):
        pass

    if not isinstance(value, (list, tuple)):
        raise ValidationError("This field expects an {container} or a list of {container}s.".format(
            container=container.__class__.__name__))

    value = validate.Length(min=min_length, max=max_length)(value)
    try:
        return [container.deserialize(v) for v in value]
    except (ValueError, TypeError):
        raise ValidationError("This field expects an {container} or a list of {container}s.".format(
            container=container.__class__.__name__))


class ObjectOrListObject(fields.Field):
    def __init__(self, cls_or_instance, min=None, max=None, **kwargs):  # noqa
        self.min = min
        self.max = max

        super(ObjectOrListObject, self).__init__(**kwargs)
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, FieldABC):
                raise ValueError('The type of the list elements '
                                 'must be a subclass of '
                                 'marshmallow.base.FieldABC')
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, FieldABC):
                raise ValueError('The instances of the list '
                                 'elements must be of type '
                                 'marshmallow.base.FieldABC')
            self.container = cls_or_instance

    def _deserialize(self, value, attr, data, **kwargs):
        return get_obj_or_list_obj(self.container, value, self.min, self.max)
