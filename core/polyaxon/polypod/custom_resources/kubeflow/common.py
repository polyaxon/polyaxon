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

from typing import Dict, Optional

from polyaxon.polypod.pod.spec import get_pod_spec, get_pod_template_spec
from polyaxon.polypod.specs.replica import ReplicaSpec


def get_kf_replicas_template(
    namespace: str,
    resource_name: str,
    replica_name: str,
    replica: Optional[ReplicaSpec],
    labels: Dict[str, str],
    template_spec: Dict,
):
    if not replica:
        return

    metadata, pod_spec = get_pod_spec(
        namespace=namespace,
        main_container=replica.main_container,
        sidecar_containers=replica.sidecar_containers,
        init_containers=replica.init_containers,
        resource_name=resource_name,
        volumes=replica.volumes,
        environment=replica.environment,
        labels=labels,
    )

    template_spec[replica_name] = {
        "replicas": replica.num_replicas,
        "restartPolicy": pod_spec.restart_policy or "Never",
        "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec),
    }
