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

from typing import Any, Optional, Tuple

from polyaxon.pql.manager import PQLManager
from polyaxon.pql.parser import parse_field
from polycommon.service_interface import Service


class QueryService(Service):
    __all__ = ("filter_queryset", "parse_field")

    @classmethod
    def filter_queryset(
        cls, manager: PQLManager, query_spec: str, queryset: Any
    ) -> Any:
        return manager.apply(query_spec=query_spec, queryset=queryset)

    @classmethod
    def parse_field(cls, field: str) -> Tuple[str, Optional[str]]:
        return parse_field(field=field)
