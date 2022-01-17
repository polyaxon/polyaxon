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
from typing import Dict

from polyaxon.exceptions import HTTP_ERROR_MESSAGES_MAPPING
from polyaxon.utils.formatting import Printer


def handle_cli_error(
    e, message: str = None, http_messages_mapping: Dict = None, sys_exit: bool = False
):
    http_messages_mapping = http_messages_mapping or {}
    if message:
        Printer.print_error(message)
    if hasattr(e, "status"):
        if e.status not in [404, 401, 403]:
            Printer.print_error("Error message: {}.".format(e))
        message = http_messages_mapping.get(
            e.status, HTTP_ERROR_MESSAGES_MAPPING.get(e.status)
        )
        Printer.print_error(message, sys_exit=sys_exit)
    elif hasattr(e, "message"):  # Handling of HTML errors
        if "404" in e.message:
            message = http_messages_mapping.get(
                404, HTTP_ERROR_MESSAGES_MAPPING.get(404)
            )
            Printer.print_error(message, sys_exit=sys_exit)
        elif "401" in e.message:
            message = http_messages_mapping.get(
                401, HTTP_ERROR_MESSAGES_MAPPING.get(401)
            )
            Printer.print_error(message, sys_exit=sys_exit)
        elif "403" in e.message:
            message = http_messages_mapping.get(
                403, HTTP_ERROR_MESSAGES_MAPPING.get(403)
            )
            Printer.print_error(message, sys_exit=sys_exit)
        else:
            Printer.print_error("Error message: {}.".format(e), sys_exit=sys_exit)
    else:
        Printer.print_error("Error message: {}.".format(e), sys_exit=sys_exit)


def handle_command_not_in_ce():
    Printer.print_error(
        "You are running Polyaxon CE which does not support this command!", True
    )
