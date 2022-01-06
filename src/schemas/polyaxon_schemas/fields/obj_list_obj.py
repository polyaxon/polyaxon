#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from marshmallow import ValidationError, fields, validate
from marshmallow.base import FieldABC


def get_obj_or_list_obj(container, value, min_length=None, max_length=None):
    try:
        return container.deserialize(value)
    except (ValueError, TypeError, ValidationError):
        pass

    if not isinstance(value, (list, tuple)):
        raise ValidationError(
            "This field expects an {container} or a list of {container}s.".format(
                container=container.__class__.__name__
            )
        )

    value = validate.Length(min=min_length, max=max_length)(value)
    try:
        return [container.deserialize(v) for v in value]
    except (ValueError, TypeError):
        raise ValidationError(
            "This field expects an {container} or a list of {container}s.".format(
                container=container.__class__.__name__
            )
        )


class ObjectOrListObject(fields.Field):
    def __init__(self, cls_or_instance, min=None, max=None, **kwargs):  # noqa
        self.min = min
        self.max = max

        super().__init__(**kwargs)
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, FieldABC):
                raise ValueError(
                    "The type of the list elements "
                    "must be a subclass of "
                    "marshmallow.base.FieldABC"
                )
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, FieldABC):
                raise ValueError(
                    "The instances of the list "
                    "elements must be of type "
                    "marshmallow.base.FieldABC"
                )
            self.container = cls_or_instance

    def _deserialize(self, value, attr, data, **kwargs):
        return get_obj_or_list_obj(self.container, value, self.min, self.max)
