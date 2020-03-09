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

import json
import os
import sys

from typing import List

from polyaxon.cli.errors import handle_cli_error
from polyaxon.containers.contexts import (
    CONTEXT_TMP_POLYAXON_PATH,
    CONTEXT_USER_POLYAXON_PATH,
)
from polyaxon.deploy.operators.docker import DockerOperator
from polyaxon.env_vars.keys import POLYAXON_KEYS_NO_OP
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.polyaxonfile import CompiledOperationSpecification
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.tracking import Run
from polyaxon.utils.formatting import Printer

POLYAXON_DATA_PATH = "/tmp/data"


def _get_env_vars(project, experiment_id, params, data_paths=None):
    env_vars = [
        ("POLYAXON_IS_MANAGED", "true"),
        ("POLYAXON_IS_LOCAL", "true"),
        (
            "POLYAXON_EXPERIMENT_INFO",
            json.dumps(
                {
                    "project_name": project,
                    "experiment_name": "{}.{}".format(project, experiment_id),
                }
            ),
        ),
    ]
    if POLYAXON_KEYS_NO_OP in os.environ:
        env_vars += [(POLYAXON_KEYS_NO_OP, "true")]
    if "POLYAXON_IS_OFFLINE" in os.environ:
        env_vars += [("POLYAXON_IS_OFFLINE", "true")]

    paths = {"local": "/tmp"}

    if data_paths:
        paths.update(data_paths)

    env_vars += [("POLYAXON_PARAMS", json.dumps(params))]
    env_vars += [("POLYAXON_RUN_DATA_PATHS", json.dumps(paths))]
    env_vars += [("POLYAXON_RUN_OUTPUTS_PATH", "/tmp/artifacts")]

    return env_vars


def _get_config_volume():
    return ["-v", "{}:{}".format(CONTEXT_USER_POLYAXON_PATH, CONTEXT_TMP_POLYAXON_PATH)]


def _get_data_bind_mounts(mount_refs=None):
    data_paths = {}
    bind_mounts = {}

    if not mount_refs:
        return data_paths, bind_mounts

    for dpath in mount_refs:
        parts = dpath.split(":")
        if len(parts) >= 2:
            ref = parts[1]
            data_ref_path = os.path.join(POLYAXON_DATA_PATH, ref)
            host_path = os.path.abspath(os.path.expanduser(parts[0]))
            data_paths[ref] = data_ref_path
            bind_mounts[host_path] = data_ref_path
        else:
            # we have just data ref name
            ref = parts[0]
            data_ref_path = os.path.join(POLYAXON_DATA_PATH, ref)
            data_paths[ref] = data_ref_path
    return data_paths, bind_mounts


def _get_data_volumes(bind_mounts):
    result = []
    for host_path, mount_path in bind_mounts.items():
        result += ["-v", "{}:{}".format(host_path, mount_path)]
    return result


def _create_docker_build(*args):
    return ""


def _run(ctx, name, owner, project_name, description, tags, specification, log):
    docker = DockerOperator()
    if not docker.check():
        raise PolyaxonException("Docker is required to run this command.")

    # Create Build
    project = "{}.{}".format(owner, project_name)
    build_job = Run(project=project)

    specification = CompiledOperationSpecification.apply_context(specification)
    content = specification.to_dict(dump=True)
    build_job.create(name=name, description=description, tags=tags, content=content)
    image = _create_docker_build(build_job, specification, project)

    experiment = Run(project=project)
    experiment.create(name=name, tags=tags, description=description, content=content)

    cmd_args = ["run", "--rm"]
    data_paths, bind_mounts = _get_data_bind_mounts(specification.data_refs)
    for key, value in _get_env_vars(
        project=project,
        experiment_id=experiment.experiment_id,
        params=specification.params,
        data_paths=data_paths,
    ):
        cmd_args += ["-e", "{key}={value}".format(key=key, value=value)]
    cmd_args += _get_config_volume()
    cmd_args += _get_data_volumes(bind_mounts)
    cmd_args += [image]

    # Add cmd.run
    _, args = specification.container.get_container_command_args()
    for arg in args:
        cmd_args += arg
    try:
        print(cmd_args)
        docker.execute(cmd_args, stream=True)
    except Exception as e:
        handle_cli_error(e, message="Could start local run.")
        sys.exit(1)


def run(
    ctx,
    name: str,
    owner: str,
    project_name: str,
    description: str,
    tags: List[str],
    compiled_operation: V1CompiledOperation,
    log: bool,
):
    try:
        _run(ctx, name, owner, project_name, description, tags, compiled_operation, log)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        handle_cli_error(e, message="Could start local run.")
        sys.exit(1)
    except Exception as e:
        Printer.print_error("Could start local run.")
        Printer.print_error("Unexpected Error: `{}`.".format(e))
        sys.exit(1)
