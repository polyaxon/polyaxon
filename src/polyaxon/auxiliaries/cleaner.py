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
import os

from typing import List

from polyaxon import pkg
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.containers.pull_policy import PullPolicy
from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.k8s_schemas import V1Container
from polyaxon.schemas.types import V1ConnectionType


def get_default_cleaner_container(
    store: V1ConnectionType, run_uuid: str, run_kind: str
):
    subpath = os.path.join(store.store_path, run_uuid)

    clean_args = "polyaxon clean-artifacts {} --subpath={}".format(
        store.kind.replace("_", "-"), subpath
    )
    wait_args = "polyaxon wait --uuid={} --kind={}".format(run_uuid, run_kind)
    return V1Container(
        name=MAIN_JOB_CONTAINER,
        image="polyaxon/polyaxon-init:{}".format(pkg.VERSION),
        image_pull_policy=PullPolicy.IF_NOT_PRESENT.value,
        command=["/bin/bash", "-c"],
        args=["{} && {}".format(wait_args, clean_args)],
        resources=k8s_schemas.V1ResourceRequirements(
            limits={"cpu": "0.5", "memory": "160Mi"},
            requests={"cpu": "0.1", "memory": "80Mi"},
        ),
    )


def get_batch_cleaner_container(
    store: V1ConnectionType,
    paths: List[str],
):
    subpaths = [os.path.join(store.store_path, subpath) for subpath in paths]
    subpaths = " ".join(["-sp={}".format(sp) for sp in subpaths])

    clean_args = "polyaxon clean-artifacts {} {}".format(
        store.kind.replace("_", "-"), subpaths
    )
    return V1Container(
        name=MAIN_JOB_CONTAINER,
        image="polyaxon/polyaxon-init:{}".format(pkg.VERSION),
        image_pull_policy=PullPolicy.IF_NOT_PRESENT.value,
        command=["/bin/bash", "-c"],
        args=[clean_args],
        resources=k8s_schemas.V1ResourceRequirements(
            limits={"cpu": "0.5", "memory": "160Mi"},
            requests={"cpu": "0.1", "memory": "80Mi"},
        ),
    )
