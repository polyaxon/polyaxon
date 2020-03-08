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

import itertools

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class ForSchema(BaseCamelSchema):
    class Meta:
        ordered = True
        fields = ("len", "do", "index")

    @staticmethod
    def schema_config():
        return ForConfig


class ForConfig(BaseConfig):
    SCHEMA = ForSchema
    IDENTIFIER = "for"

    def __init__(self, len, do, index="index"):  # noqa, redefined-builtin `len`
        self.len = len
        self.do = do
        self.index = index

    def parse(self, parser, params):
        parsed_data = []
        length = parser.parse_expression(self.len, params, check_operators=True)
        length = int(length)
        for i in range(length):
            i_params = {self.index: i}
            i_params.update(params)
            parsed_data.append(
                parser.parse_expression(self.do, i_params, check_operators=True)
            )
        if parsed_data and isinstance(parsed_data[0], (list, tuple)):
            return list(itertools.chain.from_iterable(parsed_data))
        return parsed_data


class IfSchema(BaseCamelSchema):
    class Meta:
        ordered = True
        fields = ("cond", "do", "else_do")

    @staticmethod
    def schema_config():
        return IfConfig


class IfConfig(BaseConfig):
    SCHEMA = IfSchema
    IDENTIFIER = "if"

    def __init__(self, cond, do, else_do=None):
        self.cond = cond
        self.do = do
        self.else_do = else_do

    @staticmethod
    def _check_cond(parser, cond):
        cond_template = "{{% if {} %}}1{{% else %}}0{{% endif %}}"
        cond_result = parser.parse_expression(cond_template.format(cond), {})
        if int(cond_result) == 1:
            return True
        return False

    def parse(self, parser, params):
        cond = parser.parse_expression(self.cond, params, check_operators=False)
        if self._check_cond(parser, cond):
            return parser.parse_expression(self.do, params, check_operators=True)
        if self.else_do:
            return parser.parse_expression(self.else_do, params, check_operators=True)
