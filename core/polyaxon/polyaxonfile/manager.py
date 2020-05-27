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
import copy
import os

from collections import Mapping
from typing import Dict, Union

from polyaxon import pkg
from polyaxon.exceptions import PolyaxonfileError
from polyaxon.polyaxonfile.specs import (
    CompiledOperationSpecification,
    OperationSpecification,
    get_specification,
    kinds,
)
from polyaxon.polyflow import V1Component, V1Operation

DEFAULT_POLYAXON_FILE_NAME = [
    "polyaxon",
    "polyaxonci",
    "polyaxon-ci",
    "polyaxon.ci",
    "polyaxonfile",
]

DEFAULT_POLYAXON_FILE_EXTENSION = ["yaml", "yml", "json"]


def check_default_path(path):
    path = os.path.abspath(path)
    for filename in DEFAULT_POLYAXON_FILE_NAME:
        for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
            filepath = os.path.join(path, "{}.{}".format(filename, ext))
            if os.path.isfile(filepath):
                return filepath


def get_op_specification(
    config: Union[V1Component, V1Operation] = None,
    hub: str = None,
    params: Dict = None,
    profile: str = None,
    queue: str = None,
    nocache: bool = None,
    path_context: str = None,
) -> V1Operation:
    job_data = {
        "version": config.version if config else pkg.SCHEMA_VERSION,
        "kind": kinds.OPERATION,
    }
    if params:
        if not isinstance(params, Mapping):
            raise PolyaxonfileError(
                "Params: `{}` must be a valid mapping".format(params)
            )
        job_data["params"] = params
    if profile:
        job_data["profile"] = profile
    if queue:
        job_data["queue"] = queue
    if nocache is not None:
        job_data["cache"] = {"disable": nocache}

    if config and config.kind == kinds.COMPONENT:
        job_data["component"] = config.to_dict()
        config = get_specification(data=[job_data])
    elif config and config.kind == kinds.OPERATION:
        config = get_specification(data=[config.to_dict(), job_data])
    elif hub:
        job_data["hubRef"] = hub
        config = get_specification(data=[job_data])

    if hub and config.hub_ref is None:
        config.hub_ref = hub
    hub = config.hub_ref
    public_hub = config.has_public_hub_reference
    params = copy.deepcopy(config.params)
    # Sanity check if params were passed and we are not dealing with a hub component
    if not (hub and not public_hub):
        run_config = OperationSpecification.compile_operation(config)
        run_config.validate_params(params=params, is_template=False)
        if run_config.is_dag_run:
            run_config.run.set_path_context(path_context)
            CompiledOperationSpecification.apply_context(run_config)
    return config
