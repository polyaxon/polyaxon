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

from typing import Dict, List

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.utils.formatting import Printer
from polyaxon.utils.np_utils import sanitize_np_types
from polyaxon.logger import logger


def handle_iteration(
    iteration: int = None, suggestions: List[Dict] = None, error: str = None
):
    if not settings.CLIENT_CONFIG.no_api:
        try:
            owner, project, run_uuid = get_run_info()
        except PolyaxonClientException as e:
            raise PolyaxonContainerException(e)

    def sanitize_suggestion(s: Dict):
        return {k: sanitize_np_types(v) for k, v in s.items()}

    def create_iteration_lineage():
        artifact_run = V1RunArtifact(
            name="iteration-{}".format(iteration),
            kind=V1ArtifactKind.ITERATION,
            summary={
                "iteration": iteration,
                "suggestions": [sanitize_suggestion(s) for s in suggestions]
            },
            is_input=False,
        )
        RunClient(owner=owner, project=project, run_uuid=run_uuid).log_artifact_lineage(
            artifact_run
        )

    def notify_iteration_succeeded():
        RunClient(
            owner=owner, project=project, run_uuid=run_uuid
        ).log_succeeded(message="Iterative operation has succeeded")

    def notify_iteration_failed(traceback):
        RunClient(
            owner=owner, project=project, run_uuid=run_uuid
        ).log_failed(message="Iterative operation has succeeded", traceback=traceback)

    retry = 1
    while retry < 3:
        try:
            if error:
                notify_iteration_failed(error)
                Printer.print_success("Iterative optimization failed")
                return

            if suggestions:
                create_iteration_lineage()
                Printer.print_success("Generated new suggestions generated.")
            else:
                notify_iteration_succeeded()
                Printer.print_success("Iterative optimization succeeded")
            return
        except Exception as e:
            retry += 1
            error = "Polyaxon tuner failed syncing with API, retrying, error %s" % e
            logger.warning(error)
