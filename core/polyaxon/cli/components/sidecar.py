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

import click

from polyaxon.logger import logger
from polyaxon.utils.coroutine import coroutine


@click.command()
@click.option(
    "--container-id",
    help="The tagged image destination $PROJECT/$IMAGE:$TAG.",
)
@click.option(
    "--max-retries",
    type=int,
    default=3,
    help="Number of times to retry the process.",
)
@click.option(
    "--sleep-interval",
    type=int,
    default=2,
    help="Sleep interval between retries in seconds.",
)
@click.option(
    "--sync-interval",
    type=int,
    default=-1,
    help="Interval between artifacts syncs in seconds.",
)
@click.option(
    "--monitor-logs",
    is_flag=True,
    default=False,
    help="Enable logs monitoring.",
)
@coroutine
async def sidecar(
    container_id, max_retries, sleep_interval, sync_interval, monitor_logs
):
    """
    Start Polyaxon's sidecar command.
    """
    from polyaxon.sidecar import start_sidecar

    retry = 1
    while retry < max_retries:
        try:
            await start_sidecar(
                container_id=container_id,
                sleep_interval=sleep_interval,
                sync_interval=sync_interval,
                monitor_outputs=True,
                monitor_logs=monitor_logs,
            )
            return
        except Exception as e:
            logger.warning("Polyaxon sidecar retrying, error %s", e)
            retry += 1
            await asyncio.sleep(retry)
