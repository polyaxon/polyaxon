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

from typing import Any

from polycommon.conf.exceptions import ConfException
from polycommon.conf.handler import BaseConfHandler
from polycommon.options.option import Option


class SettingsConfHandler(BaseConfHandler):
    def __init__(self):
        from django.conf import settings

        self.settings = settings

    def get(self, option: Option, **kwargs) -> Any:  # pylint:disable=arguments-differ
        if hasattr(self.settings, option.key):
            return getattr(self.settings, option.key)
        if not option.is_optional:
            raise ConfException(
                "The config option `{}` was not found or not correctly "
                "set on the settings backend.".format(option.key)
            )
        return option.default_value()

    def set(  # pylint:disable=arguments-differ
        self, option: Option, value: Any, **kwargs
    ) -> None:
        raise ConfException(
            "The settings backend does not allow to set values, "
            "are you sure the key `{}` was correctly defined.".format(option.key)
        )

    def delete(  # pylint:disable=arguments-differ
        self, option: Option, **kwargs
    ) -> None:
        raise ConfException(
            "The settings backend does not allow to delete values, "
            "are you sure the key `{}` was correctly defined.".format(option.key)
        )
