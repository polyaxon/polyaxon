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

from polyaxon.exceptions import HTTP_ERROR_MESSAGES_MAPPING
from polyaxon.utils.formatting import Printer


def handle_cli_error(e, message=None, sys_exit: bool = False):
    if message:
        Printer.print_error(message)
    if hasattr(e, "status"):
        Printer.print_error("Error message: {}.".format(e))
        Printer.print_error(
            HTTP_ERROR_MESSAGES_MAPPING.get(e.status), sys_exit=sys_exit
        )
    else:
        Printer.print_error("Error message: {}.".format(e), sys_exit=sys_exit)
