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

from typing import Tuple

from polyaxon.utils.manager_interface import ManagerInterface
from polycommon.options.option import Option


class OptionManager(ManagerInterface):
    def _get_state_data(  # pylint:disable=arguments-differ
        self, option: Option
    ) -> Tuple[str, Option]:
        return option.key, option

    def subscribe(self, option: Option) -> None:  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeOption)
        """
        super().subscribe(obj=option)

    def get(self, key: str) -> Option:  # pylint:disable=arguments-differ
        return super().get(key=key)
