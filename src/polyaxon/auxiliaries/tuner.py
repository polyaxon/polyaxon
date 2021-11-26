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
from polyaxon import pkg
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.containers.pull_policy import PullPolicy
from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.k8s_schemas import V1Container


def get_default_tuner_container(command, bracket_iteration: int = None):
    args = [
        "{{params.matrix.as_arg}}",
        "{{params.join.as_arg}}",
        "{{params.iteration.as_arg}}",
    ]
    if bracket_iteration is not None:
        args.append("{{params.bracket_iteration.as_arg}}")
    return V1Container(
        name=MAIN_JOB_CONTAINER,
        image="polyaxon/polyaxon-hpsearch:{}".format(pkg.VERSION),
        image_pull_policy=PullPolicy.IF_NOT_PRESENT.value,
        command=command,
        args=args,
        resources=k8s_schemas.V1ResourceRequirements(
            requests={"cpu": "0.1", "memory": "180Mi"},
        ),
    )
