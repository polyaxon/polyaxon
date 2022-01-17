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

from polyaxon.k8s.custom_resources.crd import get_custom_object

KIND = "Operation"
PLURAL = "operations"
API_VERSION = "v1"
GROUP = "core.polyaxon.com"


def get_operation_custom_object(
    resource_name: str,
    namespace: str,
    custom_object: Dict,
    annotations: Dict[str, str],
    labels: Dict[str, str],
) -> Dict:
    return get_custom_object(
        resource_name=resource_name,
        namespace=namespace,
        kind=KIND,
        api_version="{}/{}".format(GROUP, API_VERSION),
        labels=labels,
        annotations=annotations,
        custom_object=custom_object,
    )
