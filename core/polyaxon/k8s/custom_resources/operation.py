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

from typing import Dict

from polyaxon.k8s.custom_resources.crd import get_custom_object

KIND = "Operation"
PLURAL = "operations"
API_VERSION = "v1"
GROUP = "core.polyaxon.com"


def get_operation_custom_object(
    resource_name: str, namespace: str, custom_object: Dict, labels: Dict[str, str]
) -> Dict:
    return get_custom_object(
        resource_name=resource_name,
        namespace=namespace,
        kind=KIND,
        api_version="{}/{}".format(GROUP, API_VERSION),
        labels=labels,
        custom_object=custom_object,
    )


def get_run_instance(owner: str, project: str, run_uuid: str) -> str:
    return "{}.{}.runs.{}".format(owner, project, run_uuid)


def get_notifier_instance(owner: str, project: str, run_uuid: str) -> str:
    return "{}.{}.notifiers.{}".format(owner, project, run_uuid)


def get_resource_name(run_uuid: str) -> str:
    return "plx-operation-{}".format(run_uuid)


def get_notifier_resource_name(run_uuid: str) -> str:
    return "plx-notifier-{}".format(run_uuid)
