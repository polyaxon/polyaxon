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
import sys
import time

import click

from polyaxon.exceptions import PolyaxonAgentError
from polyaxon.logger import logger


@click.group()
def agent():
    pass


@agent.command()
@click.option(
    "--sleep-interval",
    type=int,
    help="Sleep interval between fetches (Applied only to base agent).",
)
@click.option(
    "--max-retries", type=int, default=3, help="Number of times to retry the process.",
)
def start(max_retries, sleep_interval):
    from polyaxon import settings
    from polyaxon.agents.agent import Agent
    from polyaxon.agents.base import BaseAgent
    from polyaxon.env_vars.getters import get_agent_info

    settings.CLIENT_CONFIG.set_agent_header()
    owner, agent_uuid = None, None
    is_base = True
    try:
        owner, agent_uuid = get_agent_info()
        is_base = False
        logger.info("Using agent with info: {}, {}".format(owner, agent_uuid))
    except PolyaxonAgentError:
        logger.info("Using base agent")

    def start_agent():
        if is_base:
            BaseAgent(sleep_interval=sleep_interval).start()
        else:
            Agent(owner=owner, agent_uuid=agent_uuid).start()

    retry = 1
    while retry < max_retries:
        try:
            start_agent()
            return
        except Exception as e:
            logger.warning("Polyaxon agent retrying, error %s", e)
            retry += 1
            time.sleep(5 * retry)


@agent.command()
@click.option(
    "--health-interval", type=int, help="Health interval between checks.",
)
def healthz(health_interval):
    from polyaxon.agents.base import BaseAgent

    if not BaseAgent.pong(interval=health_interval):
        logger.warning("Polyaxon agent is not healthy!")
        sys.exit(1)
