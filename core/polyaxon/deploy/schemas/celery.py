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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class CelerySchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    task_track_started = fields.Bool(allow_none=True)
    broker_pool_limit = fields.Int(allow_none=True)
    confirm_publish = fields.Bool(allow_none=True)
    worker_prefetch_multiplier = fields.Int(allow_none=True)
    worker_max_tasks_per_child = fields.Int(allow_none=True)
    worker_max_memory_per_child = fields.Int(allow_none=True)
    task_always_eager = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return CeleryConfig


class CeleryConfig(BaseConfig):
    SCHEMA = CelerySchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "taskTrackStarted",
        "brokerPoolLimit",
        "confirmPublish",
        "workerPrefetchMultiplier",
        "workerMaxTasksPerChild",
        "workerMaxMemoryPerChild",
        "taskAlwaysEager",
    ]

    def __init__(
        self,
        enabled=None,
        task_track_started=None,
        broker_pool_limit=None,
        confirm_publish=None,
        worker_prefetch_multiplier=None,
        worker_max_tasks_per_child=None,
        worker_max_memory_per_child=None,
        task_always_eager=None,
    ):
        self.enabled = enabled
        self.task_track_started = task_track_started
        self.broker_pool_limit = broker_pool_limit
        self.confirm_publish = confirm_publish
        self.worker_prefetch_multiplier = worker_prefetch_multiplier
        self.worker_max_tasks_per_child = worker_max_tasks_per_child
        self.worker_max_memory_per_child = worker_max_memory_per_child
        self.task_always_eager = task_always_eager
