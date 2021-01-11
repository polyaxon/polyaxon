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

import sys

from polyaxon.constants import DEFAULT
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.managers.user import UserConfigManager
from polyaxon.utils.formatting import Printer


def get_local_owner(is_cli: bool = False):
    from polyaxon import settings

    owner = None
    if UserConfigManager.is_initialized():
        try:
            user_config = UserConfigManager.get_config()
            owner = user_config.organization
        except TypeError:
            Printer.print_error(
                "Found an invalid user config or user config cache, "
                "if you are using Polyaxon CLI please run: "
                "`polyaxon config purge --cache-only`",
                sys_exit=True,
            )

    if not owner and (not settings.CLI_CONFIG or settings.CLI_CONFIG.is_ce):
        owner = DEFAULT

    if not owner:
        if is_cli:
            Printer.print_error("An owner is required.")
            sys.exit(1)
        else:
            raise PolyaxonClientException("An owner is required.")
    return owner
