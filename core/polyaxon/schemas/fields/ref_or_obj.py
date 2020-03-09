#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from marshmallow import ValidationError, fields
from marshmallow.base import FieldABC

from polyaxon.schemas.fields.params import PARAM_REGEX


def get_ref_or_obj(container, value):
    try:
        return container.deserialize(value)
    except (ValueError, TypeError, ValidationError):
        pass

    if not isinstance(value, str):
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

        super().__init__(allow_none=True, **kwargs)
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
        if isinstance(value, str):
            param = PARAM_REGEX.search(value)
            if not param:
                super()._validate(value)
        else:
            super()._validate(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return get_ref_or_obj(self.container, value)
