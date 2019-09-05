# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
import warnings

from hestia.list_utils import to_list
from marshmallow import ValidationError, fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class OutputsContextSchema(BaseSchema):
    enable = fields.Bool(allow_none=True)
    manage = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return OutputsContextConfig


class OutputsContextConfig(BaseConfig):
    IDENTIFIER = "outputs_context"
    SCHEMA = OutputsContextSchema
    REDUCED_ATTRIBUTES = ["enable", "manage"]

    def __init__(self, enable=None, manage=None):
        self.enable = enable
        self.manage = manage
