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

import traceback

from typing import Dict, List

from polyaxon.client import RunClient
from polyaxon.logger import logger
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyflow import V1Join
from polyaxon.utils.formatting import Printer
from polyaxon.utils.np_utils import sanitize_dict, sanitize_np_types


def get_iteration_definition(
    client: RunClient,
    iteration: int,
    join: V1Join,
    optimization_metric: str,
    name: str = None,
):
    def handler():
        runs = (
            client.list(
                query=join.query,
                sort=join.sort,
                limit=join.limit,
                offset=join.offset,
            ).results
            or []
        )
        configs = []
        metrics = []
        run_uuids = []
        for run in runs:
            if optimization_metric in run.outputs:
                run_uuids.append(run.uuid)
                configs.append(run.inputs)
                metrics.append(run.outputs[optimization_metric])

        if configs or metrics or run_uuids:
            artifact_run = V1RunArtifact(
                name=name or "in-iteration-{}".format(iteration),
                kind=V1ArtifactKind.ITERATION,
                summary={
                    "iteration": iteration,
                    "configs": [sanitize_dict(s) for s in configs],
                    "metrics": [sanitize_np_types(s) for s in metrics],
                    "uuid": run_uuids,
                },
                is_input=True,
            )
            client.log_artifact_lineage(artifact_run)

        return run_uuids, configs, metrics

    try:
        return handler()
    except Exception as e:
        exp = "Polyaxon tuner failed fetching iteration definition: {}\n{}".format(
            repr(e), traceback.format_exc()
        )
        client.log_failed(reason="PolyaxonTunerIteration", message=exp)
        logger.warning(e)


def handle_iteration_failure(client: RunClient, exp: Exception):
    exp = "Polyaxon tuner failed creating suggestions : {}\n{}".format(
        repr(exp), traceback.format_exc()
    )
    client.log_failed(reason="PolyaxonTunerSuggestions", message=exp)


def handle_iteration(
    client: RunClient,
    iteration: int = None,
    suggestions: List[Dict] = None,
    summary: Dict = None,
    name: str = None,
):
    summary = summary or {}
    summary.update(
        {
            "iteration": iteration,
            "suggestions": [sanitize_dict(s) for s in suggestions],
        }
    )

    def handler():
        if suggestions:
            artifact_run = V1RunArtifact(
                name=name or "out-iteration-{}".format(iteration),
                kind=V1ArtifactKind.ITERATION,
                summary=summary,
                is_input=False,
            )
            client.log_artifact_lineage(artifact_run)
            Printer.print_success("Tuner generated new suggestions.")
        else:
            client.log_succeeded(message="Iterative operation has succeeded")
            Printer.print_success("Iterative optimization succeeded")

    try:
        handler()
    except Exception as e:
        exp = "Polyaxon tuner failed logging iteration definition: {}\n{}".format(
            repr(e), traceback.format_exc()
        )
        client.log_failed(reason="PolyaxonTunerIteration", message=exp)
        logger.warning(e)
