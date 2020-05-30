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

from typing import Dict


class Result:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SEVERITY_VALUES = {INFO, WARNING, ERROR}

    def __init__(self, message="Service is healthy", severity=INFO) -> None:
        self.message = message
        if severity not in self.SEVERITY_VALUES:
            raise ValueError("Health check Error not recognized `{}`".format(severity))
        self.severity = severity

    def __str__(self) -> str:
        return self.message

    @property
    def is_healthy(self) -> bool:
        return self.severity == self.INFO

    @property
    def is_warning(self) -> bool:
        return self.severity == self.WARNING

    @property
    def is_error(self) -> bool:
        return self.severity == self.ERROR

    def to_dict(self) -> Dict:
        return {
            "is_healthy": self.is_healthy,
            "message": self.message,
            "severity": self.severity,
        }
