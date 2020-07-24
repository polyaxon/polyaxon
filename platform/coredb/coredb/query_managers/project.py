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

from coredb.query_managers.manager import BaseQueryManager
from polyaxon.pql.builder import (
    ArrayCondition,
    BoolCondition,
    DateTimeCondition,
    SearchCondition,
    ValueCondition,
)
from polyaxon.pql.parser import (
    parse_datetime_operation,
    parse_search_operation,
    parse_value_operation,
)


class ProjectQueryManager(BaseQueryManager):
    NAME = "project"
    FIELDS_PROXY = {
        "id": "uuid",
        "uid": "uuid",
        "user": "user__username",
        "archived": "deleted",
    }
    FIELDS_ORDERING = ("created_at", "updated_at", "name", "user")
    CHECK_ALIVE = True
    PARSERS_BY_FIELD = {
        # Uuid
        "id": parse_search_operation,
        "uid": parse_search_operation,
        "uuid": parse_search_operation,
        # Dates
        "created_at": parse_datetime_operation,
        "updated_at": parse_datetime_operation,
        # Name
        "name": parse_search_operation,
        # Description
        "description": parse_search_operation,
        # Tags
        "tags": parse_value_operation,
        # User
        "user": parse_value_operation,
        # Archived
        "archived": parse_value_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Uuid
        "id": SearchCondition,
        "uid": SearchCondition,
        "uuid": SearchCondition,
        # Dates
        "created_at": DateTimeCondition,
        "updated_at": DateTimeCondition,
        # Name
        "name": SearchCondition,
        # Description
        "description": SearchCondition,
        # User
        "user": ValueCondition,
        # Tags
        "tags": ArrayCondition,
        # archived
        "archived": BoolCondition,
    }
