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

from typing import List, Optional, Tuple

from kubernetes_asyncio.client.rest import ApiException

from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.types import AwareDT
from polyaxon.utils.tz_utils import now


def get_label_selector(operation: str) -> str:
    return "app.kubernetes.io/instance={},app.kubernetes.io/managed-by=polyaxon".format(
        operation
    )


async def get_k8s_operation_logs(
    k8s_manager: AsyncK8SManager,
    operation: str,
    last_time: Optional[AwareDT],
    stream: bool = False,
) -> Tuple[List[V1Log], Optional[AwareDT]]:

    new_time = now()
    params = {}
    if last_time:
        since_seconds = (new_time - last_time).total_seconds() - 1
        params["since_seconds"] = int(since_seconds)
    if stream:
        params["tail_lines"] = V1Logs.CHUNK_SIZE
    logs = []

    pods = await k8s_manager.list_pods(labels=get_label_selector(operation))

    async def handle_container_logs():
        resp = None
        try:
            resp = await k8s_manager.k8s_api.read_namespaced_pod_log(
                pod.metadata.name,
                k8s_manager.namespace,
                container=container.name,
                timestamps=True,
                **params,
            )
        except ApiException:
            pass
        if not resp:
            return None, None

        for log_line in resp.split("\n"):
            if log_line:
                logs.append(
                    V1Log.process_log_line(
                        value=log_line,
                        node=pod.spec.node_name,
                        pod=pod.metadata.name,
                        container=container.name,
                    )
                )

    for pod in pods:
        for container in pod.spec.init_containers or []:
            await handle_container_logs()
        for container in pod.spec.containers or []:
            await handle_container_logs()

    if logs:
        last_time = logs[-1].timestamp
    return logs, last_time
