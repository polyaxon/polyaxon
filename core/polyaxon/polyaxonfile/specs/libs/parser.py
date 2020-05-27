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

import ast
import copy
import jinja2

from collections import Mapping
from typing import Dict

from polyaxon.config_reader.utils import deep_update
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile.specs.sections import Sections
from polyaxon.polyflow import ParamSpec

try:
    import numpy as np
except (ImportError, ModuleNotFoundError):
    np = None


class Parser(object):
    """Parses the Polyaxonfile."""

    env = jinja2.Environment()

    @staticmethod
    def _get_section_data(section_data):
        if hasattr(section_data, "to_dict"):
            return section_data.to_dict()
        return section_data

    @classmethod
    def _get_section(cls, config, section):
        if not hasattr(config, section):
            return None
        section_data = getattr(config, section)
        if isinstance(section_data, list):
            return [cls._get_section_data(d) for d in section_data]

        return cls._get_section_data(section_data)

    @classmethod
    def parse(
        cls, config, params: Dict[str, ParamSpec]
    ):  # pylint:disable=too-many-branches
        params = params or {}
        parsed_params = {param: params[param].display_value for param in params}

        parsed_data = {Sections.VERSION: config.version, Sections.KIND: config.kind}

        if config.name:
            parsed_data[Sections.NAME] = config.name
        if config.description:
            parsed_data[Sections.DESCRIPTION] = config.description
        if config.tags:
            parsed_data[Sections.TAGS] = config.tags
        inputs = getattr(config, Sections.INPUTS)
        if inputs:
            parsed_data[Sections.INPUTS] = [io.to_dict() for io in inputs]
        outputs = getattr(config, Sections.OUTPUTS)
        if outputs:
            parsed_data[Sections.OUTPUTS] = [
                cls.parse_expression(io.to_dict(), parsed_params) for io in outputs
            ]

        # Check workflow
        matrix_section = cls._get_section(config, Sections.MATRIX)
        if matrix_section:
            parsed_data[Sections.MATRIX] = cls.parse_expression(
                matrix_section, parsed_params
            )
            matrix_params = copy.copy(parsed_data[Sections.MATRIX])
            if matrix_params:
                parsed_params = deep_update(matrix_params, parsed_params)

        for section in Sections.PARSING_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(
                    config_section, parsed_params
                )

        for section in Sections.OP_PARSING_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(
                    config_section, parsed_params
                )

        config_section = cls._get_section(config, Sections.RUN)
        if config_section:
            parsed_data[Sections.RUN] = config_section

        return parsed_data

    @classmethod
    def parse_run(cls, parsed_data, params: Dict[str, ParamSpec]):
        config_section = cls.parse_section(
            parsed_data.get(Sections.RUN), params=params, parse_params=True
        )
        if config_section:
            parsed_data[Sections.RUN] = config_section
        return parsed_data

    @classmethod
    def parse_section(
        cls, config_section, params: Dict[str, ParamSpec], parse_params: bool = True
    ):
        params = params or {}
        if parse_params:
            params = {param: params[param].display_value for param in params}
        if config_section:
            return cls.parse_expression(config_section, params)
        return config_section

    @classmethod
    def parse_expression(  # pylint:disable=too-many-branches
        cls, expression, params: Dict, check_operators: bool = False
    ):
        try:
            return cls._parse_expression(expression, params, check_operators)
        except jinja2.exceptions.TemplateError as e:
            raise PolyaxonSchemaError(
                "An problem parsing the template, please make sure your variables are resolvable. "
                "Error: {}".format(repr(e))
            )

    @classmethod
    def _parse_expression(  # pylint:disable=too-many-branches
        cls, expression, params: Dict, check_operators: bool = False
    ):
        if isinstance(expression, (int, float, complex, type(None))):
            return expression
        if np and isinstance(expression, np.integer):
            return int(expression)
        if np and isinstance(expression, np.floating):
            return float(expression)
        if isinstance(expression, Mapping):
            if len(expression) == 1:
                old_key, value = list(expression.items())[0]
                # always parse the keys, they must be base object or evaluate to base objects
                key = cls._parse_expression(old_key, params)
                if check_operators and cls.is_operator(key):
                    return cls._parse_operator({key: value}, params)
                else:
                    return {key: cls.parse_expression(value, params, check_operators)}

            new_expression = {}
            for k, v in expression.items():
                new_expression.update(
                    cls._parse_expression({k: v}, params, check_operators)
                )
            return new_expression

        if isinstance(expression, list):
            return list(
                cls.parse_expression(v, params, check_operators) for v in expression
            )
        if isinstance(expression, tuple):
            return tuple(
                cls.parse_expression(v, params, check_operators) for v in expression
            )
        if isinstance(expression, str):
            return cls._evaluate_expression(expression, params, check_operators)

    @classmethod
    def _evaluate_expression(cls, expression, params, check_operators):
        result = cls.env.from_string(expression).render(**params)
        if result == expression:
            try:
                return ast.literal_eval(result)
            except (ValueError, SyntaxError):
                pass
            return result
        return cls.parse_expression(result, params, check_operators)

    @classmethod
    def _parse_operator(cls, expression, params):
        k, v = list(expression.items())[0]
        op = Sections.OPERATORS[k].from_dict(v)
        return op.parse(parser=cls, params=params)

    @staticmethod
    def is_operator(key):
        return key in Sections.OPERATORS
