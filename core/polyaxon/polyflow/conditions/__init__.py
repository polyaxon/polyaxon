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

from polyaxon.polyflow.conditions.io import IoCondSchema, V1IoCond
from polyaxon.polyflow.conditions.status import StatusCondSchema, V1StatusCond
from polyaxon.schemas.base import BaseOneOfSchema


class ConditionSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1StatusCond.IDENTIFIER: StatusCondSchema,
        V1IoCond.IDENTIFIER: IoCondSchema,
    }
