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

from coredb.query_managers.manager import BaseQueryManager
from polyaxon.pql.builder import BoolCondition, SearchCondition, ValueCondition
from polyaxon.pql.parser import parse_search_operation, parse_value_operation


class ArtifactQueryManager(BaseQueryManager):
    NAME = "artifact"
    FIELDS_ORDERING = ("name", "kind", "path", "is_input")
    FIELDS_USE_UUID = {"run"}
    FIELDS_PROXY = {
        "id": "name",
        "name": "artifact__name",
        "kind": "artifact__kind",
        "path": "artifact__path",
        "state": "artifact__state",
    }
    CHECK_ALIVE = False
    DISTINCT = False
    PARSERS_BY_FIELD = {
        # Name
        "name": parse_search_operation,
        # Kind
        "kind": parse_value_operation,
        # Path
        "path": parse_value_operation,
        # State
        "state": parse_value_operation,
        # Is input
        "is_input": parse_value_operation,
        # Run
        "run": parse_value_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Name
        "name": SearchCondition,
        # Kind
        "kind": ValueCondition,
        # Path
        "path": ValueCondition,
        # State
        "state": ValueCondition,
        # Is input
        "is_input": BoolCondition,
        # Run
        "run": ValueCondition,
    }
