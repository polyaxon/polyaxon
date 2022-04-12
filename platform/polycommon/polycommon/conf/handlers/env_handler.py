#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

import os

from typing import Any

from polycommon.conf.exceptions import ConfException
from polycommon.conf.handler import BaseConfHandler
from polycommon.options.option import Option


class EnvConfHandler(BaseConfHandler):
    def get(self, option: Option, **kwargs) -> Any:  # pylint:disable=arguments-differ
        value = os.environ.get(option.key)
        if value:
            return option.parse(value)
        if not option.is_optional:
            raise ConfException(
                "The config option `{}` was not found or not correctly "
                "set on the settings backend.".format(option.key)
            )
        return option.default_value()

    def set(  # pylint:disable=arguments-differ
        self, option: Option, value: Any, **kwargs
    ) -> None:
        os.environ[option.key] = str(value)

    def delete(  # pylint:disable=arguments-differ
        self, option: Option, **kwargs
    ) -> None:
        os.environ.pop(option.key, None)
