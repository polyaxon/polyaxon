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

from typing import Dict

from polyaxon.k8s import k8s_schemas


def get_custom_object(
    namespace: str,
    resource_name: str,
    kind: str,
    api_version: str,
    labels: Dict,
    annotations: Dict,
    custom_object: Dict,
) -> Dict:
    metadata = k8s_schemas.V1ObjectMeta(
        name=resource_name,
        labels=labels,
        annotations=annotations,
        namespace=namespace,
    )
    custom_object.update(
        {"kind": kind, "apiVersion": api_version, "metadata": metadata}
    )

    return custom_object
