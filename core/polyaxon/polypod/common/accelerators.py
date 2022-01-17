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

from typing import Dict, Union

from polyaxon.k8s import k8s_schemas


def has_tpu_annotation(annotations: Dict) -> bool:
    if not annotations:
        return False
    for key in annotations.keys():
        if "tpu" in key:
            return True

    return False


def requests_tpu(resources: Union[k8s_schemas.V1ResourceRequirements, Dict]) -> bool:
    if not resources:
        return False

    if not isinstance(resources, k8s_schemas.V1ResourceRequirements):
        resources = k8s_schemas.V1ResourceRequirements(**resources)

    if resources.requests:
        for key in resources.requests.keys():
            if "tpu" in key:
                return True

    if resources.limits:
        for key in resources.limits.keys():
            if "tpu" in key:
                return True

    return False


def requests_gpu(resources: k8s_schemas.V1ResourceRequirements) -> bool:
    if not resources:
        return False

    if resources.requests:
        for key in resources.requests.keys():
            if "gpu" in key:
                return True

    if resources.limits:
        for key in resources.limits.keys():
            if "gpu" in key:
                return True

    return False
