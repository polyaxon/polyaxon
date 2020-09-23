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

from polyaxon_sdk import V1Run

from polyaxon.managers.base import BaseConfigManager
from polyaxon.utils.formatting import Printer


class RunConfigManager(BaseConfigManager):
    """Manages run configuration .run file."""

    VISIBILITY = BaseConfigManager.VISIBILITY_ALL
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = ".run"
    CONFIG = V1Run

    @classmethod
    def get_config_or_raise(cls):
        run = cls.get_config()
        if not run:
            Printer.print_error("No run was provided.")
            sys.exit(1)

        return run
