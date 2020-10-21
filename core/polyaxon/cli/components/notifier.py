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

import click


@click.command()
@click.option(
    "--kind",
    help="The notification kind.",
)
@click.option(
    "--owner",
    help="The project owner.",
)
@click.option(
    "--project",
    help="The project containing the operation.",
)
@click.option("--run-uuid", help="The run uuid.")
@click.option("--run-name", help="The run name.")
@click.option(
    "--condition",
    help="The run condition to notify.",
)
def notify(kind, owner, project, run_uuid, run_name, condition):
    """Notifier command."""
    import ujson

    from polyaxon.lifecycle import V1StatusCondition
    from polyaxon.notifiers import NOTIFIERS, NotificationSpec

    condition = ujson.loads(condition)
    condition = V1StatusCondition.get_condition(**condition)
    notification = NotificationSpec(
        kind=kind,
        owner=owner,
        project=project,
        uuid=run_uuid,
        name=run_name,
        condition=condition,
    )
    NOTIFIERS[kind].execute(notification=notification)
