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

import ast
import jinja2

from collections.abc import Mapping
from typing import Dict

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile.specs.libs.engine import get_engine
from polyaxon.polyaxonfile.specs.sections import Sections
from polyaxon.polyflow import ParamSpec

try:
    import numpy as np
except (ImportError, ModuleNotFoundError):
    np = None


class Parser:
    """Parses the Polyaxonfile."""

    engine = get_engine()

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

    @staticmethod
    def get_parsed_params(param_spec: Dict[str, ParamSpec]) -> Dict:
        parsed_params = {"params": {}}
        as_arg = []
        for param in param_spec or {}:
            parsed_params[param] = param_spec[param].get_display_value()
            # Add params level
            if not param_spec[param].is_context:
                as_arg.append(param_spec[param].as_arg())
                parsed_params["params"][param] = param_spec[param].to_parsed_param()

        parsed_params["params"]["as_args"] = [a for a in as_arg if a]
        return parsed_params

    @classmethod
    def parse_operation(
        cls, config, param_spec: Dict[str, ParamSpec]
    ):  # pylint:disable=too-many-branches
        parsed_params = cls.get_parsed_params(param_spec)

        parsed_data = {Sections.VERSION: config.version, Sections.KIND: config.kind}

        if config.name:
            parsed_data[Sections.NAME] = config.name
        if config.description:
            parsed_data[Sections.DESCRIPTION] = config.description
        if config.tags:
            parsed_data[Sections.TAGS] = config.tags
        contexts = getattr(config, Sections.CONTEXTS)
        if contexts:
            parsed_data[Sections.CONTEXTS] = [
                cls.parse_io(io.to_dict(), parsed_params) for io in contexts
            ]
        inputs = getattr(config, Sections.INPUTS)
        if inputs:
            parsed_data[Sections.INPUTS] = [
                cls.parse_io(io.to_dict(), parsed_params) for io in inputs
            ]
        outputs = getattr(config, Sections.OUTPUTS)
        if outputs:
            parsed_data[Sections.OUTPUTS] = [
                cls.parse_io(io.to_dict(), parsed_params) for io in outputs
            ]

        # Check workflow
        for section in Sections.PARSING_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(
                    config_section, parsed_params
                )

        parsed_data = cls._parse_conditions(parsed_data)

        config_section = cls._get_section(config, Sections.RUN)
        if config_section:
            parsed_data[Sections.RUN] = config_section
        config_section = cls._get_section(config, Sections.HOOKS)
        if config_section:
            parsed_data[Sections.HOOKS] = config_section

        return parsed_data

    @classmethod
    def _parse_conditions(cls, parsed_data: Dict) -> Dict:
        if Sections.CONDITIONS in parsed_data and not isinstance(
            parsed_data[Sections.CONDITIONS], str
        ):
            parsed_data[Sections.CONDITIONS] = str(parsed_data[Sections.CONDITIONS])
        if Sections.SKIP_ON_UPSTREAM_SKIP in parsed_data and not isinstance(
            parsed_data[Sections.SKIP_ON_UPSTREAM_SKIP], str
        ):
            parsed_data[Sections.SKIP_ON_UPSTREAM_SKIP] = str(
                parsed_data[Sections.SKIP_ON_UPSTREAM_SKIP]
            )
        if Sections.IS_APPROVED in parsed_data and not isinstance(
            parsed_data[Sections.IS_APPROVED], str
        ):
            parsed_data[Sections.IS_APPROVED] = str(parsed_data[Sections.IS_APPROVED])
        return parsed_data

    @classmethod
    def _parse_hook(cls, config, param_spec: Dict[str, ParamSpec]):
        hook = cls.parse_section(config, param_spec=param_spec, parse_params=True)
        return cls._parse_conditions(hook)

    @classmethod
    def parse_hooks(cls, config, param_spec: Dict[str, ParamSpec]):
        hooks = config.hooks or []
        return [
            cls._parse_hook(hook.to_dict(), param_spec=param_spec) for hook in hooks
        ]

    @classmethod
    def parse_runtime(cls, parsed_data, param_spec: Dict[str, ParamSpec]):
        config_section = cls.parse_section(
            parsed_data.get(Sections.RUN), param_spec=param_spec, parse_params=True
        )
        if config_section:
            parsed_data[Sections.RUN] = config_section
        return parsed_data

    @classmethod
    def parse_distributed_runtime(
        cls, parsed_data, param_spec: Dict[str, Dict[str, ParamSpec]]
    ):
        run_section = parsed_data.get(Sections.RUN)
        config_section = {}
        for k in run_section:
            if k in param_spec:
                config_section[k] = cls.parse_section(
                    run_section[k], param_spec=param_spec[k], parse_params=True
                )
            else:
                config_section[k] = run_section[k]
        if config_section:
            parsed_data[Sections.RUN] = config_section
        return parsed_data

    @classmethod
    def parse_section(
        cls, config_section, param_spec: Dict[str, ParamSpec], parse_params: bool = True
    ):
        if parse_params:
            param_spec = cls.get_parsed_params(param_spec)
        if config_section:
            return cls.parse_expression(config_section, param_spec)
        return config_section

    @classmethod
    def parse_io(
        cls,
        expression: Dict,
        params: Dict[str, ParamSpec],
        check_operators: bool = False,
    ):
        # Arg format should not be converted
        arg_format = expression.pop("argFormat", None)
        value = cls.parse_expression(expression, params, check_operators)
        if arg_format:
            value["argFormat"] = arg_format
        return value

    @classmethod
    def parse_expression(  # pylint:disable=too-many-branches
        cls, expression, params: Dict, check_operators: bool = False
    ):
        try:
            return cls._parse_expression(expression, params, check_operators)
        except jinja2.exceptions.TemplateError as e:
            raise PolyaxonSchemaError(
                "Encountered a problem parsing the template, "
                "please make sure your variables are resolvable. "
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
        try:
            result = cls.engine.from_string(expression).render(**params)
        except (ValueError, TypeError) as e:
            raise PolyaxonSchemaError(
                "Encountered a problem parsing the template, "
                "please make sure your variables are resolvable. "
                "Error: {}".format(repr(e))
            )
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
