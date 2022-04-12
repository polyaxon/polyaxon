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

from typing import Any, Dict, Optional

from polycommon.options.option import Option


class BaseConfHandler:
    def get(self, option: Option, owners: Optional[Dict[str, int]] = None) -> Any:
        raise NotImplementedError

    def set(
        self, option: Option, value: Any, owners: Optional[Dict[str, int]] = None
    ) -> None:
        raise NotImplementedError

    def delete(self, option: Option, owners: Optional[Dict[str, int]] = None) -> Any:
        raise NotImplementedError
