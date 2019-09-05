# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
import warnings

from hestia.list_utils import to_list
from marshmallow import ValidationError, fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class EnableSchema(BaseSchema):
    enable = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return EnableConfig


class EnableConfig(BaseConfig):
    IDENTIFIER = "enable"
    SCHEMA = EnableSchema
    REDUCED_ATTRIBUTES = ["enable"]

    def __init__(self, enable=None):
        self.enable = enable
