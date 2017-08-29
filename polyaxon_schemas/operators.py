# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import itertools

from marshmallow import Schema, post_load

from polyaxon_schemas.base import BaseConfig


class ForSchema(Schema):
    class Meta:
        ordered = True
        fields = ('len', 'do', 'index')

    @post_load
    def make(self, data):
        return ForConfig(**data)


class ForConfig(BaseConfig):
    SCHEMA = ForSchema
    IDENTIFIER = 'for'

    def __init__(self, len, do, index='index'):
        self.len = len
        self.do = do
        self.index = index

    def parse(self, parser, declarations):
        parsed_data = []
        length = parser.parse_expression(self.len, declarations, check_operators=True)
        length = int(length)
        for i in range(length):
            i_declarations = {self.index: i}
            i_declarations.update(declarations)
            parsed_data.append(
                parser.parse_expression(self.do, i_declarations, check_operators=True))
        if parsed_data and isinstance(parsed_data[0], (list, tuple)):
            return list(itertools.chain.from_iterable(parsed_data))
        return parsed_data


class IfSchema(Schema):

    class Meta:
        ordered = True
        fields = ('cond', 'do', 'else_do')

    @post_load
    def make(self, data):
        return IfConfig(**data)


class IfConfig(BaseConfig):
    SCHEMA = IfSchema
    IDENTIFIER = 'if'

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

    def parse(self, parser, declarations):
        cond = parser.parse_expression(self.cond, declarations, check_operators=False)
        if self._check_cond(parser, cond):
            return parser.parse_expression(self.do, declarations, check_operators=True)
        if self.else_do:
            return parser.parse_expression(self.else_do, declarations, check_operators=True)
