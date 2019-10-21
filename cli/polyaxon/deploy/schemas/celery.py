#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class CelerySchema(BaseSchema):
    taskTrackStarted = fields.Bool(allow_none=True)
    brokerPoolLimit = fields.Int(allow_none=True)
    confirmPublish = fields.Bool(allow_none=True)
    workerPrefetchMultiplier = fields.Int(allow_none=True)
    workerMaxTasksPerChild = fields.Int(allow_none=True)
    workerMaxMemoryPerChild = fields.Int(allow_none=True)
    taskAlwaysEager = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return CeleryConfig


class CeleryConfig(BaseConfig):
    SCHEMA = CelerySchema
    REDUCED_ATTRIBUTES = [
        "taskTrackStarted",
        "brokerPoolLimit",
        "confirmPublish",
        "workerPrefetchMultiplier",
        "workerMaxTasksPerChild",
        "workerMaxMemoryPerChild",
        "taskAlwaysEager",
    ]

    def __init__(
        self,  # noqa
        taskTrackStarted=None,
        brokerPoolLimit=None,
        confirmPublish=None,
        workerPrefetchMultiplier=None,
        workerMaxTasksPerChild=None,
        workerMaxMemoryPerChild=None,
        taskAlwaysEager=None,
    ):
        self.taskTrackStarted = taskTrackStarted
        self.brokerPoolLimit = brokerPoolLimit
        self.confirmPublish = confirmPublish
        self.workerPrefetchMultiplier = workerPrefetchMultiplier
        self.workerMaxTasksPerChild = workerMaxTasksPerChild
        self.workerMaxMemoryPerChild = workerMaxMemoryPerChild
        self.taskAlwaysEager = taskAlwaysEager
