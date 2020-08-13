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

from typing import Dict, List, Optional

from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.custom_resources.operation import get_operation_custom_object
from polyaxon.polyflow import V1Environment, V1Notification, V1Termination
from polyaxon.polypod.common.setter import (
    set_collect_logs,
    set_notify,
    set_sync_statuses,
    set_termination,
)
from polyaxon.polypod.pod.spec import get_pod_spec, get_pod_template_spec


def get_job_custom_resource(
    resource_name: str,
    namespace: str,
    main_container: k8s_schemas.V1Container,
    sidecar_containers: Optional[List[k8s_schemas.V1Container]],
    init_containers: Optional[List[k8s_schemas.V1Container]],
    volumes: List[k8s_schemas.V1Volume],
    termination: V1Termination,
    collect_logs: bool,
    sync_statuses: bool,
    notifications: List[V1Notification],
    environment: V1Environment,
    labels: Dict[str, str],
    annotations: Dict[str, str],
) -> Dict:
    metadata, pod_spec = get_pod_spec(
        namespace=namespace,
        main_container=main_container,
        sidecar_containers=sidecar_containers,
        init_containers=init_containers,
        resource_name=resource_name,
        volumes=volumes,
        environment=environment,
        labels=labels,
    )

    template_spec = {
        "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec)
    }

    custom_object = {"batchJobSpec": template_spec}
    custom_object = set_termination(
        custom_object=custom_object, termination=termination
    )
    custom_object = set_collect_logs(
        custom_object=custom_object, collect_logs=collect_logs
    )
    custom_object = set_sync_statuses(
        custom_object=custom_object, sync_statuses=sync_statuses
    )
    custom_object = set_notify(custom_object=custom_object, notifications=notifications)

    return get_operation_custom_object(
        namespace=namespace,
        resource_name=resource_name,
        labels=labels,
        annotations=annotations,
        custom_object=custom_object,
    )
