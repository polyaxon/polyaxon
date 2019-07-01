# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.utils.formatting import Printer


def parse_params(params):
    parsed_params = {}
    for param in params:
        index = param.find("=")
        if index == -1:
            Printer.print_error("Invalid format for -P parameter: '%s'. Use -P name=value." % param)
            sys.exit(1)
        name = param[:index]
        value = param[index + 1:]
        if name in parsed_params:
            Printer.print_error("Repeated parameter: '%s'" % name)
            sys.exit(1)
        parsed_params[name] = value

    return parsed_params
