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

import click

from polyaxon.logger import clean_outputs, logger


@click.command()
@click.option(
    "--container_id",
    "--container-id",
    help="The tagged image destination $PROJECT/$IMAGE:$TAG.",
)
@click.option(
    "--max_retries",
    "--max-retries",
    type=int,
    default=3,
    help="Number of times to retry the process.",
)
@click.option(
    "--sleep_interval",
    "--sleep-interval",
    type=int,
    default=2,
    help="Sleep interval between retries in seconds.",
)
@click.option(
    "--sync_interval",
    "--sync-interval",
    type=int,
    default=-1,
    help="Interval between artifacts syncs in seconds.",
)
@clean_outputs
def sidecar(container_id, max_retries, sleep_interval, sync_interval):
    """
    Start Polyaxon's sidecar command.
    """
    from polyaxon.sidecar import start_sidecar

    retry = 1
    while retry < max_retries:
        try:
            start_sidecar(
                container_id=container_id,
                sleep_interval=sleep_interval,
                sync_interval=sync_interval,
                monitor_outputs=True,
                monitor_logs=False,
            )
            return
        except Exception as e:
            logger.warning("Polyaxon sidecar retrying, error %s", e)
            retry += 1
            time.sleep(1 * retry)
