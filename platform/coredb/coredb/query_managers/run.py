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
from coredb.query_managers import callback_conditions
from coredb.query_managers.manager import BaseQueryManager
from polyaxon.pql.builder import (
    ArrayCondition,
    BoolCondition,
    CallbackCondition,
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
    FIELDS_USE_UUID = {
        "project",
        "original",
        "upstream",
        "downstream",
        "pipeline",
        "controller",
        "agent",
        "queue",
        "artifacts_store",
    }
    FIELDS_PROXY = {
        "params": "inputs",
        "in": "inputs",
        "out": "outputs",
        "metrics": "outputs",
        "meta_values": "meta_info",
        "meta_flags": "meta_info",
        "id": "uuid",
        "uid": "uuid",
        "user": "user__username",
        "agent": "agent__name",
        "queue": "queue__name",
        "artifacts_store": "artifacts_store__name",
        "upstream": "upstream_runs__uuid",
        "downstream": "downstream_runs__uuid",
    }
    FIELDS_ORDERING = (
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
        "schedule_at",
        "name",
        "kind",
        "runtime",
        "user",
        "uuid",
        "duration",
        "wait_time",
        "status",
    )
    FIELDS_ORDERING_PROXY = {
        "metrics": {"field": "outputs", "annotate": True},
        "params": {"field": "inputs", "annotate": True},
        "inputs": {"field": "inputs", "annotate": True},
        "in": {"field": "inputs", "annotate": True},
        "outputs": {"field": "outputs", "annotate": True},
        "out": {"field": "outputs", "annotate": True},
        "meta_flags": {"field": "meta_info", "annotate": True},
        "meta_info": {"field": "meta_info", "annotate": True},
        "meta_values": {"field": "meta_info", "annotate": True},
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
        "schedule_at": parse_datetime_operation,
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
        # Controller
        "controller": parse_value_operation,
        # Upstream
        "upstream": parse_value_operation,
        # Downstream
        "downstream": parse_value_operation,
        # Cloning kind
        "cloning_kind": parse_value_operation,
        # Artifact
        "in_artifact_kind": parse_value_operation,
        "out_artifact_kind": parse_value_operation,
        # Backend
        "backend": parse_value_operation,
        # Framework
        "framework": parse_value_operation,
        # Commit
        "commit": parse_value_operation,
        # Kind
        "kind": parse_value_operation,
        # Meta Kind
        "runtime": parse_value_operation,
        # Params
        "params": parse_value_operation,
        "inputs": parse_value_operation,
        "in": parse_value_operation,
        # Results
        "outputs": parse_value_operation,
        "out": parse_value_operation,
        # Metrics
        "metrics": parse_scalar_operation,
        # Meta
        "meta_flags": parse_value_operation,
        "meta_info": parse_value_operation,
        "meta_values": parse_scalar_operation,
        # Tags
        "tags": parse_value_operation,
        # Live state
        "live_state": parse_value_operation,
        # Duration
        "duration": parse_scalar_operation,
        # Wait time
        "wait_time": parse_scalar_operation,
        # Agent
        "agent": parse_value_operation,
        "queue": parse_value_operation,
        # Artifacts store
        "artifacts_store": parse_value_operation,
        # Flags
        "is_managed": parse_value_operation,
        "pending": parse_value_operation,
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
        "schedule_at": DateTimeCondition,
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
        # Controller
        "controller": ValueCondition,
        # Upstream
        "upstream": ValueCondition,
        # Downstream
        "downstream": ValueCondition,
        # Cloning kind
        "cloning_kind": ValueCondition,
        # Artifact
        "in_artifact_kind": CallbackCondition(
            callback_conditions.in_artifact_kind_condition
        ),
        "out_artifact_kind": CallbackCondition(
            callback_conditions.in_artifact_kind_condition
        ),
        # Backend
        "backend": ValueCondition,
        # Framework
        "framework": ValueCondition,
        # Commit
        "commit": CallbackCondition(callback_conditions.commit_condition),
        # Kind
        "kind": ValueCondition,
        # Meta Kind
        "runtime": ValueCondition,
        # Params
        "params": ValueCondition,
        "inputs": ValueCondition,
        "in": ValueCondition,
        # Results
        "outputs": ValueCondition,
        "out": ValueCondition,
        # Metrics
        "metrics": ComparisonCondition,
        # Meta
        "meta_flags": BoolCondition,
        "meta_info": ValueCondition,
        "meta_values": ValueCondition,
        # Tags
        "tags": ArrayCondition,
        # Live state
        "live_state": ValueCondition,
        # Duration
        "duration": ComparisonCondition,
        # Wait time
        "wait_time": ComparisonCondition,
        # Agent
        "agent": ValueCondition,
        "queue": ValueCondition,
        # Artifacts store
        "artifacts_store": ValueCondition,
        # Flags
        "is_managed": BoolCondition,
        "pending": ValueCondition,
    }
