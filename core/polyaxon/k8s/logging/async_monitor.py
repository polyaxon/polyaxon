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

from typing import List, Optional, Tuple

from kubernetes_asyncio.client.models import V1Pod
from kubernetes_asyncio.client.rest import ApiException

from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.types import AwareDT
from polyaxon.utils.tz_utils import now


def get_label_selector(instance: str) -> str:
    return "app.kubernetes.io/instance={},app.kubernetes.io/managed-by=polyaxon".format(
        instance
    )


async def handle_container_logs(
    k8s_manager: AsyncK8SManager, pod: V1Pod, container_name: str, **params
) -> List[V1Log]:
    resp = None
    try:
        resp = await k8s_manager.k8s_api.read_namespaced_pod_log(
            pod.metadata.name,
            k8s_manager.namespace,
            container=container_name,
            timestamps=True,
            **params,
        )
    except ApiException:
        pass
    if not resp:
        return []

    logs = []
    for log_line in resp.split("\n"):
        if log_line:
            logs.append(
                V1Log.process_log_line(
                    value=log_line,
                    node=pod.spec.node_name,
                    pod=pod.metadata.name,
                    container=container_name,
                )
            )
    return logs


async def handle_pod_logs(
    k8s_manager: AsyncK8SManager, pod: V1Pod, **params
) -> List[V1Log]:
    logs = []
    for container in pod.spec.init_containers or []:
        logs += await handle_container_logs(
            k8s_manager=k8s_manager, pod=pod, container_name=container.name, **params
        )
    for container in pod.spec.containers or []:
        logs += await handle_container_logs(
            k8s_manager=k8s_manager, pod=pod, container_name=container.name, **params
        )
    return logs


async def query_k8s_operation_logs(
    k8s_manager: AsyncK8SManager,
    instance: str,
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

    pods = await k8s_manager.list_pods(label_selector=get_label_selector(instance))

    for pod in pods:
        logs += await handle_pod_logs(
            k8s_manager=k8s_manager,
            pod=pod,
            **params,
        )

    if logs:
        last_time = logs[-1].timestamp
    return logs, last_time


async def query_k8s_pod_logs(
    k8s_manager: AsyncK8SManager,
    pod: V1Pod,
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

    logs = await handle_pod_logs(k8s_manager=k8s_manager, pod=pod, **params)

    if logs:
        last_time = logs[-1].timestamp
    return logs, last_time
