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

from collections import namedtuple
from datetime import timedelta
from typing import Any, Optional

from django.utils import timezone

from polyaxon.types import AwareDT
from polycommon.options.option_owners import OptionOwners


class CachedOptionSpec(namedtuple("CachedOptionSpec", "value datetime")):
    pass


class MemoryCacheManager:
    INVALIDED_OPTION = "INVALIDED_OPTION"

    def __init__(self):
        self._state = {}

    def clear_key(self, key: str, owners: Optional[OptionOwners] = None) -> None:
        if owners:
            key = f"{key}:{owners}"
        self._state.pop(key, None)

    def clear(self) -> None:
        self._state = {}

    @classmethod
    def is_valid_value(cls, value: Any):
        return value != cls.INVALIDED_OPTION

    @staticmethod
    def is_valid_cache(value_datetime: AwareDT) -> bool:
        return timezone.now() < value_datetime

    def get_from_cache(self, key: str, owners: Optional[OptionOwners] = None) -> Any:
        if owners:
            key = f"{key}:{owners}"
        cached_option = self._state.get(key)
        if cached_option and self.is_valid_cache(cached_option.datetime):
            return cached_option.value
        self.clear_key(key=key)
        return self.INVALIDED_OPTION

    def set_to_cache(
        self, key: str, value: Any, ttl: int, owners: Optional[OptionOwners] = None
    ) -> None:
        if ttl <= 0 or value is None:
            return
        if owners:
            key = f"{key}:{owners}"
        self._state[key] = CachedOptionSpec(
            value=value, datetime=timezone.now() + timedelta(seconds=ttl)
        )
