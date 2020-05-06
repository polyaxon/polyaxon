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
from typing import List

import ujson

from polyaxon import settings
from polyaxon.agents.spawners.async_spawner import AsyncSpawner
from polyaxon.lifecycle import V1StatusCondition
from polyaxon.logger import logger
from polyaxon.operations import get_notifier_operation
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.polypod import compiler


async def notify_run(
    namespace: str,
    owner: str,
    project: str,
    run_uuid: str,
    run_name: str,
    condition: V1StatusCondition,
    connections: List[str],
):
    spawner = AsyncSpawner(namespace=namespace)
    await spawner.k8s_manager.setup()
    for connection in connections:
        connection_type = settings.AGENT_CONFIG.notification_connections_by_names.get(
            connection
        )
        if not connection_type:
            logger.warning(
                "Could not create notification using connection {}, "
                "the connection was not found or not set correctly.".format(
                    connection_type
                )
            )
            continue

        operation = get_notifier_operation(
            connection=connection,
            kind=connection_type.kind,
            owner=owner,
            project=project,
            run_uuid=run_uuid,
            run_name=run_name,
            condition=ujson.dumps(condition.to_dict()),
        )
        compiled_operation = OperationSpecification.compile_operation(operation)
        resource = compiler.make(
            owner_name=owner,
            project_name=project,
            project_uuid=project,
            run_uuid=run_uuid,
            run_name=run_name,
            run_path=run_uuid,
            compiled_operation=compiled_operation,
            params=operation.params,
        )
        await spawner.create(
            run_uuid=run_uuid,
            run_kind=compiled_operation.get_run_kind(),
            resource=resource,
        )
