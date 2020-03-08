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

from polyaxon.utils.list_utils import to_list
from polyaxon.utils.string_utils import strip_spaces


def get_container_command_args(config):
    def sanitize_str(value):
        if not value:
            return
        value = strip_spaces(value=value, join=False)
        value = [c.strip().strip("\\") for c in value if (c and c != "\\")]
        value = [c for c in value if (c and c != "\\")]
        return " ".join(value)

    def sanitize(value):
        return (
            [sanitize_str(v) for v in value]
            if isinstance(value, list)
            else to_list(sanitize_str(value), check_none=True)
        )

    return to_list(config.command, check_none=True), sanitize(config.args)
