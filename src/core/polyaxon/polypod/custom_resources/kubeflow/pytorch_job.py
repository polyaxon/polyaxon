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

from typing import Dict, List, Optional

from polyaxon.k8s.custom_resources.operation import get_operation_custom_object
from polyaxon.polyflow import V1Notification, V1SchedulingPolicy, V1Termination
from polyaxon.polypod.common.setter import (
    set_clean_pod_policy,
    set_collect_logs,
    set_notify,
    set_scheduling_policy,
    set_sync_statuses,
    set_termination,
)
from polyaxon.polypod.custom_resources.kubeflow.common import get_kf_replicas_template
from polyaxon.polypod.specs.replica import ReplicaSpec


def get_pytorch_job_custom_resource(
    resource_name: str,
    namespace: str,
    master: Optional[ReplicaSpec],
    worker: Optional[ReplicaSpec],
    termination: V1Termination,
    collect_logs: bool,
    sync_statuses: bool,
    notifications: List[V1Notification],
    clean_pod_policy: Optional[str],
    scheduling_policy: Optional[V1SchedulingPolicy],
    labels: Dict[str, str],
    annotations: Dict[str, str],
) -> Dict:
    template_spec = {}

    get_kf_replicas_template(
        replica_name="Master",
        replica=master,
        namespace=namespace,
        resource_name=resource_name,
        labels=labels,
        annotations=annotations,
        template_spec=template_spec,
    )
    get_kf_replicas_template(
        replica_name="Worker",
        replica=worker,
        namespace=namespace,
        resource_name=resource_name,
        labels=labels,
        annotations=annotations,
        template_spec=template_spec,
    )
    template_spec = {"replicaSpecs": template_spec}

    template_spec = set_clean_pod_policy(
        template_spec=template_spec, clean_pod_policy=clean_pod_policy
    )

    template_spec = set_scheduling_policy(
        template_spec=template_spec, scheduling_policy=scheduling_policy
    )

    custom_object = {"pytorchJobSpec": template_spec}
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
