#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.schemas.base import BaseConfig, BaseSchema


class Optimization(object):
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"

    MAXIMIZE_VALUES = [MAXIMIZE, MAXIMIZE.upper(), MAXIMIZE.capitalize()]
    MINIMIZE_VALUES = [MINIMIZE, MINIMIZE.upper(), MINIMIZE.capitalize()]

    VALUES = MAXIMIZE_VALUES + MINIMIZE_VALUES

    @classmethod
    def maximize(cls, value):
        return value in cls.MAXIMIZE_VALUES

    @classmethod
    def minimize(cls, value):
        return value in cls.MINIMIZE_VALUES


class SearchMetricSchema(BaseSchema):
    name = fields.Str()
    optimization = fields.Str(
        allow_none=True, validate=validate.OneOf(Optimization.VALUES)
    )

    @staticmethod
    def schema_config():
        return SearchMetricConfig


class SearchMetricConfig(BaseConfig):
    SCHEMA = SearchMetricSchema
    IDENTIFIER = "search_metric"

    def __init__(self, name, optimization=Optimization.MAXIMIZE):
        self.name = name
        self.optimization = optimization
