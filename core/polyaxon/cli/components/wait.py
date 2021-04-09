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

import sys
import time

import click


@click.command()
@click.option("--uuid", help="The operation's run uuid.")
@click.option(
    "--kind",
    help="The operation kind.",
)
@click.option(
    "--max-retries",
    type=int,
    default=10,
    help="Number of times to retry the process.",
)
def wait(uuid: str, kind: str, max_retries: int):
    """Delete an s3 subpath."""
    from polyaxon import settings
    from polyaxon.agents.spawners.spawner import Spawner

    spawner = Spawner(namespace=settings.CLIENT_CONFIG.namespace, in_cluster=True)
    retry = 1
    while retry < max_retries:
        try:
            k8s_operation = spawner.get(run_uuid=uuid, run_kind=kind)
        except Exception:  # noqa
            k8s_operation = None
        if k8s_operation:
            retry += 1
            time.sleep(retry)
        else:
            return

    sys.exit(1)
