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
import asyncio
import os

from kubernetes.client.rest import ApiException

from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.env_vars.keys import POLYAXON_KEYS_K8S_POD_ID
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.logger import logger
from polyaxon.settings import CLIENT_CONFIG
from polyaxon.sidecar.intervals import get_sync_interval
from polyaxon.sidecar.monitors import sync_artifacts, sync_logs, sync_summaries


async def start_sidecar(
    container_id: str,
    sleep_interval: int,
    sync_interval: int,
    monitor_outputs: bool,
    monitor_logs: bool,
):
    sync_interval = get_sync_interval(
        interval=sync_interval, sleep_interval=sleep_interval
    )
    try:
        pod_id = os.environ[POLYAXON_KEYS_K8S_POD_ID]
    except KeyError as e:
        raise PolyaxonContainerException(
            "Please make sure that this job has been "
            "started by Polyaxon with all required context."
        ) from e

    try:
        owner, project, run_uuid = get_run_info()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)

    client = RunClient(owner=owner, project=project, run_uuid=run_uuid)
    k8s_manager = AsyncK8SManager(namespace=CLIENT_CONFIG.namespace, in_cluster=True)
    await k8s_manager.setup()
    pod = await k8s_manager.get_pod(pod_id, reraise=True)

    retry = 1
    is_running = True
    counter = 0
    state = {
        "last_artifacts_check": None,
        "last_logs_check": None,
    }

    async def monitor():
        if monitor_logs:
            await sync_logs(
                run_uuid=run_uuid,
                k8s_manager=k8s_manager,
                pod=pod,
                last_time=None,
                stream=True,
                is_running=is_running,
            )
        if monitor_outputs:
            last_check = state["last_artifacts_check"]
            state["last_artifacts_check"] = sync_artifacts(
                last_check=last_check,
                run_uuid=run_uuid,
            )
            sync_summaries(
                last_check=last_check,
                run_uuid=run_uuid,
                client=client,
            )

    while is_running and retry <= 3:
        await asyncio.sleep(sleep_interval)
        try:
            is_running = await k8s_manager.is_pod_running(pod_id, container_id)
        except ApiException as e:
            retry += 1
            logger.info("Exception %s" % repr(e))
            logger.info("Sleeping ...")
            await asyncio.sleep(retry)
            continue

        logger.debug("Syncing ...")
        if is_running:
            retry = 1

        counter += 1
        if counter == sync_interval:
            counter = 0
            try:
                await monitor()
            except Exception as e:
                logger.warning("Polyaxon sidecar error: %s" % repr(e))

    await monitor()
    logger.info("Cleaning non main containers")
    if k8s_manager:
        await k8s_manager.close()
