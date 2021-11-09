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

import click

from polyaxon.cli.options import OPTIONS_NAME


@click.command()
@click.option(
    "--backend",
    help="The notifier backend.",
)
@click.option(
    "--owner",
    help="The project owner.",
)
@click.option(
    "--project",
    help="The project containing the operation.",
)
@click.option("--uuid", help="The run uuid.")
@click.option(*OPTIONS_NAME["args"], help="The run name.")
@click.option(
    "--kind",
    help="The operation kind.",
)
@click.option(
    "--condition",
    help="The run's condition.",
)
@click.option(
    "--status",
    help="The run status.",
)
@click.option(
    "--wait-time",
    "--wait_time",
    help="The run wait_time.",
)
@click.option(
    "--duration",
    help="The run duration.",
)
@click.option(
    "--inputs",
    help="The run's inputs.",
)
@click.option(
    "--outputs",
    help="The run outputs.",
)
def notify(
    backend,
    owner,
    project,
    uuid,
    name,
    kind,
    condition,
    status,
    wait_time,
    duration,
    inputs,
    outputs,
):
    """Notifier command."""
    import ujson

    from polyaxon.lifecycle import V1StatusCondition
    from polyaxon.notifiers import NOTIFIERS, NotificationSpec

    condition = ujson.loads(condition)
    condition = V1StatusCondition.get_condition(**condition)
    status = status or condition.type
    notification = NotificationSpec(
        kind=kind,
        owner=owner,
        project=project,
        uuid=uuid,
        name=name,
        status=status,
        wait_time=wait_time,
        duration=duration,
        condition=condition,
        inputs=inputs,
        outputs=outputs,
    )
    NOTIFIERS[backend].execute(notification=notification)
