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

from polyaxon_sdk import V1Project

from polyaxon.managers.base import BaseConfigManager
from polyaxon.utils import constants
from polyaxon.utils.formatting import Printer


class ProjectManager(BaseConfigManager):
    """Manages project configuration .polyaxonproject file."""

    IS_GLOBAL = True
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = ".polyaxonproject"
    CONFIG = V1Project

    @classmethod
    def get_config_or_raise(cls):
        project = cls.get_config()
        if not project:
            Printer.print_error(
                "Please initialize your project before uploading any code."
                " {}".format(constants.INIT_COMMAND)
            )
            sys.exit(1)

        return project
