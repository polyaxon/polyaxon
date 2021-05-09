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

from polycommon.events.event import Attribute

OWNER_ATTRIBUTES = (Attribute("id"), Attribute("name"))

OWNER_RESOURCE_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("name"),
    Attribute("owner.name"),
    Attribute("owner_id"),
)

AGENT_RESOURCE_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("name"),
    Attribute("owner.name"),
    Attribute("owner_id"),
    Attribute("agent_name"),
    Attribute("agent_uuid"),
    Attribute("agent_id"),
)

PROJECT_OWNER_ATTRIBUTES = (
    Attribute("name"),
    Attribute("owner.name"),
    Attribute("owner_id"),
)

PROJECT_RESOURCE_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("project.uuid", is_uuid=True),
    Attribute("project.name"),
    Attribute("project.owner.name"),
    Attribute("name", is_required=False),
)

PROJECT_RESOURCE_OWNER_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("project.uuid", is_uuid=True),
    Attribute("project.name"),
    Attribute("project.owner.name"),
    Attribute("owner_id"),
    Attribute("name", is_required=False),
)

PROJECT_RUN_EXECUTOR_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("project.uuid", is_uuid=True),
    Attribute("project.name"),
    Attribute("project.owner.name"),
    Attribute("name", is_required=False),
    Attribute("is_managed", attr_type=bool, is_required=False),
    Attribute("pipeline_id", attr_type=int, is_required=False),
)

PROJECT_RUN_EXECUTOR_OWNER_ATTRIBUTES = (
    Attribute("uuid", is_uuid=True),
    Attribute("project.uuid", is_uuid=True),
    Attribute("project.name"),
    Attribute("owner_id"),
    Attribute("project.owner.name"),
    Attribute("name", is_required=False),
    Attribute("is_managed", attr_type=bool, is_required=False),
    Attribute("pipeline_id", attr_type=int, is_required=False),
)
