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

import sys

from polyaxon.utils.formatting import Printer


def parse_params(params):
    parsed_params = {}
    for param in params:
        index = param.find("=")
        if index == -1:
            Printer.print_error(
                "Invalid format for -P parameter: '%s'. Use -P name=value." % param
            )
            sys.exit(1)
        name = param[:index]
        value = param[index + 1 :]
        if name in parsed_params:
            Printer.print_error("Repeated parameter: '%s'" % name)
            sys.exit(1)
        parsed_params[name] = {"value": value}

    return parsed_params
