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
    ComparisonCondition,
    DateTimeCondition,
    SearchCondition,
    ValueCondition,
)
from polyaxon.pql.parser import (
    parse_datetime_operation,
    parse_scalar_operation,
    parse_search_operation,
    parse_value_operation,
)


class RunQueryManager(BaseQueryManager):
    NAME = "run"
    FIELDS_USE_UUID = {"project", "original", "pipeline"}
    FIELDS_PROXY = {
        "params": "inputs",
        "in": "inputs",
        "out": "outputs",
        "metrics": "outputs",
        "id": "uuid",
        "uid": "uuid",
        "user": "user__username",
        "archived": "deleted",
    }
    FIELDS_ORDERING = (
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "name",
        "kind",
        "user",
        "uuid",
        "run_time",
    )
    FIELDS_ORDERING_PROXY = {
        "metrics": {"field": "outputs", "annotate": True},
        "params": {"field": "inputs", "annotate": True},
        "inputs": {"field": "inputs", "annotate": True},
        "in": {"field": "inputs", "annotate": True},
        "outputs": {"field": "outputs", "annotate": True},
        "out": {"field": "outputs", "annotate": True},
    }
    FIELDS_DEFAULT_ORDERING = ("-updated_at",)
    CHECK_ALIVE = True
    PARSERS_BY_FIELD = {
        # Uuid
        "id": parse_search_operation,
        "uid": parse_search_operation,
        "uuid": parse_search_operation,
        # Dates
        "created_at": parse_datetime_operation,
        "updated_at": parse_datetime_operation,
        "started_at": parse_datetime_operation,
        "finished_at": parse_datetime_operation,
        # Name
        "name": parse_search_operation,
        # Description
        "description": parse_search_operation,
        # User
        "user": parse_value_operation,
        # Status
        "status": parse_value_operation,
        # Project
        "project": parse_value_operation,
        # Original
        "original": parse_value_operation,
        # Pipeline
        "pipeline": parse_value_operation,
        # Cloning kind
        "cloning_kind": parse_value_operation,
        # Builds
        "build": parse_value_operation,
        # Backend
        "backend": parse_value_operation,
        # Framework
        "framework": parse_value_operation,
        # Commit
        "commit": parse_value_operation,
        # Kind
        "kind": parse_value_operation,
        # Params
        "params": parse_value_operation,
        "inputs": parse_value_operation,
        "in": parse_value_operation,
        # Results
        "outputs": parse_value_operation,
        "out": parse_value_operation,
        # Metrics
        "metrics": parse_scalar_operation,
        # Tags
        "tags": parse_value_operation,
        # Archived
        "archived": parse_value_operation,
        # Run time
        "run_time": parse_scalar_operation,
    }
    CONDITIONS_BY_FIELD = {
        # Uuid
        "id": SearchCondition,
        "uid": SearchCondition,
        "uuid": SearchCondition,
        # Dates
        "created_at": DateTimeCondition,
        "updated_at": DateTimeCondition,
        "started_at": DateTimeCondition,
        "finished_at": DateTimeCondition,
        # Name
        "name": SearchCondition,
        # Description
        "description": SearchCondition,
        # User
        "user": ValueCondition,
        # Status
        "status": ValueCondition,
        # Project
        "project": ValueCondition,
        # Original
        "original": ValueCondition,
        # Pipeline
        "pipeline": ValueCondition,
        # Cloning kind
        "cloning_kind": ValueCondition,
        # Builds
        "build": ValueCondition,
        # Backend
        "backend": ValueCondition,
        # Framework
        "framework": ValueCondition,
        # Commit
        "commit": ValueCondition,
        # Kind
        "kind": ValueCondition,
        # Params
        "params": ValueCondition,
        "inputs": ValueCondition,
        "in": ValueCondition,
        # Results
        "outputs": ValueCondition,
        "out": ValueCondition,
        # Metrics
        "metrics": ComparisonCondition,
        # Tags
        "tags": ArrayCondition,
        # archived
        "archived": BoolCondition,
        # run time
        "run_time": ComparisonCondition,
    }
