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

from collections.abc import Mapping

from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.specs.libs.parser import Parser
from polyaxon.utils.formatting import Printer


def parse_params(params, is_cli: bool = True):
    if isinstance(params, Mapping):
        return {k: {"value": Parser.parse_expression(v, {})} for k, v in params.items()}

    parsed_params = {}
    for param in params:
        index = param.find("=")
        if index == -1:
            message = (
                "Invalid format for -P parameter: '%s'. Use -P name=value." % param
            )
            if is_cli:
                Printer.print_error(message, sys_exit=True)
            else:
                raise PolyaxonfileError(message)
        name = param[:index]
        value = param[index + 1 :]
        if name in parsed_params:
            message = "Repeated parameter: '%s'" % name
            if is_cli:
                Printer.print_error(message, sys_exit=True)
            else:
                raise PolyaxonfileError(message)
        parsed_params[name] = {"value": value}

    return parsed_params
