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
import traceback

from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Tuple

import polyaxon_sdk

from kubernetes.client.rest import ApiException

from polyaxon.agents import converter
from polyaxon.agents.spawners.spawner import Spawner
from polyaxon.client import PolyaxonClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolypodException
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.logger import logger
from polyaxon.utils.workers_utils import exit_context, get_pool_workers, get_wait


class BaseAgent:
    def __init__(self, sleep_interval=None):
        self.sleep_interval = sleep_interval
        self.spawner = Spawner()
        self.client = PolyaxonClient()
        self._graceful_shutdown = False

    def get_state(self) -> polyaxon_sdk.V1AgentStateResponse:
        raise NotImplementedError

    def start(self) -> None:
        try:
            with exit_context() as exit_event:
                index = 0
                workers = get_pool_workers()

                with ThreadPoolExecutor(workers) as pool:
                    logger.debug("Thread pool Workers: {}".format(workers))
                    timeout = self.sleep_interval or get_wait(index)
                    while not exit_event.wait(timeout=timeout):
                        index += 1
                        agent_state = self.process(pool)
                        if agent_state.status == V1Statuses.STOPPED:
                            self.end()
                            return
                        if agent_state.state.full:
                            index = 0
                        timeout = self.sleep_interval or get_wait(index)
                        logger.info("Sleeping for {} seconds".format(timeout))
        finally:
            self.end()

    def end(self):
        self._graceful_shutdown = True
        logger.info("Agent is shutting down.")

    def process(self, pool: "ThreadPoolExecutor") -> polyaxon_sdk.V1AgentStateResponse:
        try:
            agent_state = self.get_state()

            if agent_state:
                logger.info("Starting runs submission process.")
            else:
                logger.info("No state was found.")
                return polyaxon_sdk.V1AgentStateResponse()

            state = agent_state.state
            for run_data in state.queued or []:
                pool.submit(self.create_run, run_data)
            for run_data in state.stopping or []:
                pool.submit(self.stop_run, run_data)
            for run_data in state.apply or []:
                pool.submit(self.apply_run, run_data)
            return agent_state
        except Exception as exc:
            logger.error(exc)
            return polyaxon_sdk.V1AgentStateResponse()

    def log_run_failed(
        self,
        run_owner: str,
        run_project: str,
        run_uuid: str,
        exc: Exception,
        message: str = None,
    ) -> None:
        message = message or "Agent failed deploying run.\n"
        message += "error: {}\n{}".format(repr(exc), traceback.format_exc())
        self.log_run_status(
            run_owner=run_owner,
            run_project=run_project,
            run_uuid=run_uuid,
            status=V1Statuses.FAILED,
            reason="PolyaxonAgentRunActionFailed",
            message=message,
        )
        logger.warning(message)

    def log_run_stopped(self, run_owner: str, run_project: str, run_uuid: str) -> None:
        message = "Run was not found, so we assume it was stopped."
        self.log_run_status(
            run_owner=run_owner,
            run_project=run_project,
            run_uuid=run_uuid,
            status=V1Statuses.STOPPED,
            reason="PolyaxonAgentRunActionStopped",
            message=message,
        )
        logger.warning(message)

    def log_run_scheduled(
        self, run_owner: str, run_project: str, run_uuid: str
    ) -> None:
        message = "Run was scheduled by the agent."
        self.log_run_status(
            run_owner=run_owner,
            run_project=run_project,
            run_uuid=run_uuid,
            status=V1Statuses.SCHEDULED,
            reason="PolyaxonAgentRunActionScheduled",
            message=message,
        )
        logger.info(message)

    def log_run_running(self, run_owner: str, run_project: str, run_uuid: str) -> None:
        message = "Run changes were applied by the agent."
        self.log_run_status(
            run_owner=run_owner,
            run_project=run_project,
            run_uuid=run_uuid,
            status=V1Statuses.RUNNING,
            reason="PolyaxonAgentRunActionRunning",
            message=message,
        )
        logger.info(message)

    def log_run_status(
        self,
        run_owner: str,
        run_project: str,
        run_uuid: str,
        status: str,
        reason: str = None,
        message: str = None,
    ):
        status_condition = V1StatusCondition.get_condition(
            type=status, status=True, reason=reason, message=message
        )
        self.client.runs_v1.create_run_status(
            owner=run_owner,
            project=run_project,
            uuid=run_uuid,
            body={"condition": status_condition},
            async_req=True,
        )

    def clean_run(self, run_uuid: str, run_kind: str):
        try:
            self.spawner.stop(run_uuid=run_uuid, run_kind=run_kind)
        except ApiException as e:
            if e.status == 404:
                logger.debug("Run does not exist.")
        except Exception as e:
            logger.debug(
                "Run could not be cleaned: {}\n{}".format(
                    repr(e), traceback.format_exc()
                )
            )

    def prepare_run_resource(
        self,
        owner_name: str,
        project_name: str,
        run_name: str,
        run_uuid: str,
        content: str,
    ) -> Dict:
        try:
            return converter.convert(
                owner_name=owner_name,
                project_name=project_name,
                run_name=run_name,
                run_uuid=run_uuid,
                content=content,
                default_auth=True,
            )
        except PolypodException as e:
            self.log_run_failed(
                run_owner=owner_name,
                run_project=project_name,
                run_uuid=run_uuid,
                exc=e,
                message="Agent failed converting run manifest.\n",
            )
        except Exception as e:
            self.log_run_failed(
                run_owner=owner_name,
                run_project=project_name,
                run_uuid=run_uuid,
                exc=e,
                message="Agent failed during compilation with unknown exception.\n",
            )

    def create_run(self, run_data: Tuple[str, str, str, str]):
        run_owner, run_project, run_uuid = get_run_info(run_instance=run_data[0])
        resource = self.prepare_run_resource(
            owner_name=run_owner,
            project_name=run_project,
            run_name=run_data[2],
            run_uuid=run_uuid,
            content=run_data[3],
        )

        try:
            self.spawner.create(
                run_uuid=run_uuid, run_kind=run_data[1], resource=resource
            )
            self.log_run_scheduled(
                run_owner=run_owner, run_project=run_project, run_uuid=run_uuid
            )
        except ApiException as e:
            if e.status == 409:
                logger.info(
                    "Run already running running, triggering an apply mechanism."
                )
                self.apply_run(run_data=run_data)
            else:
                logger.info("Run submission error.")
                self.log_run_failed(
                    run_owner=run_owner,
                    run_project=run_project,
                    run_uuid=run_uuid,
                    exc=e,
                )
        except Exception as e:
            self.log_run_failed(
                run_owner=run_owner, run_project=run_project, run_uuid=run_uuid, exc=e
            )

    def apply_run(self, run_data: Tuple[str, str, str, str]):
        run_owner, run_project, run_uuid = get_run_info(run_instance=run_data[0])
        resource = self.prepare_run_resource(
            owner_name=run_owner,
            project_name=run_project,
            run_name=run_data[2],
            run_uuid=run_uuid,
            content=run_data[3],
        )

        try:
            self.spawner.apply(
                run_uuid=run_uuid, run_kind=run_data[1], resource=resource
            )
            self.log_run_running(
                run_owner=run_owner, run_project=run_project, run_uuid=run_uuid
            )
        except Exception as e:
            self.log_run_failed(
                run_owner=run_owner, run_project=run_project, run_uuid=run_uuid, exc=e
            )
            self.clean_run(run_uuid=run_uuid, run_kind=run_data[1])

    def stop_run(self, run_data: Tuple[str, str]):
        run_owner, run_project, run_uuid = get_run_info(run_instance=run_data[0])
        try:
            self.spawner.stop(run_uuid=run_uuid, run_kind=run_data[1])
        except ApiException as e:
            if e.status == 404:
                logger.info("Run does not exist anymore, it could have been stopped.")
                self.log_run_stopped(
                    run_owner=run_owner, run_project=run_project, run_uuid=run_uuid
                )
        except Exception as e:
            self.log_run_failed(
                run_owner=run_owner,
                run_project=run_project,
                run_uuid=run_uuid,
                exc=e,
                message="Agent failed stopping run.\n",
            )
