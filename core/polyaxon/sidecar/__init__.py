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

import time

from kubernetes.client.rest import ApiException

from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.k8s.manager import K8SManager
from polyaxon.k8s.monitor import is_pod_running
from polyaxon.logger import logger
from polyaxon.settings import CLIENT_CONFIG
from polyaxon.sidecar.intervals import get_sync_interval
from polyaxon.sidecar.logging import sync_logs
from polyaxon.sidecar.outputs import sync_artifacts, sync_summaries


def start_sidecar(
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
        owner, project, run_uuid = get_run_info()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)

    client = RunClient(owner=owner, project=project, run_uuid=run_uuid)
    pod_id = CLIENT_CONFIG.pod_id
    if not pod_id:
        raise PolyaxonContainerException(
            "Please make sure that this job has been "
            "started by Polyaxon with all required context."
        )

    k8s_manager = K8SManager(namespace=CLIENT_CONFIG.namespace, in_cluster=True)
    retry = 1
    is_running = True
    counter = 0
    state = {
        "last_artifacts_check": None,
        "last_logs_check": None,
    }

    def monitor():
        if monitor_outputs:
            last_check = state["last_artifacts_check"]
            state["last_artifacts_check"] = sync_artifacts(
                last_check=last_check, run_uuid=run_uuid,
            )
            sync_summaries(
                last_check=last_check, run_uuid=run_uuid, client=client,
            )

        if monitor_logs:
            state["last_logs_check"] = sync_logs(
                k8s_manager=k8s_manager,
                client=client,
                last_check=state["last_logs_check"],
                run_uuid=run_uuid,
                pod_id=pod_id,
                container_id=container_id,
                owner=owner,
                project=project,
            )

    while is_running and retry <= 3:
        time.sleep(sleep_interval)
        try:
            is_running = is_pod_running(k8s_manager, pod_id, container_id)
        except ApiException as e:
            retry += 1
            time.sleep(1 * retry)
            logger.info("Exception %s" % repr(e))
            logger.info("Sleeping ...")
            continue

        logger.debug("Syncing ...")
        if is_running:
            retry = 1

        counter += 1
        if counter == sync_interval:
            counter = 0
            try:
                monitor()
            except Exception as e:
                logger.warning("Polyaxon sidecar error: %e", e)

    monitor()
    logger.info("Cleaning non main containers")
