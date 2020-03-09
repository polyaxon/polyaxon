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

from typing import Dict, List, Optional, Tuple

from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow import V1Environment
from polyaxon.utils.list_utils import to_list


def get_pod_spec(
    resource_name: str,
    namespace: str,
    main_container: k8s_schemas.V1Container,
    sidecar_containers: Optional[List[k8s_schemas.V1Container]],
    init_containers: Optional[List[k8s_schemas.V1Container]],
    environment: Optional[V1Environment],
    labels: Dict[str, str],
    volumes: Optional[List[k8s_schemas.V1Volume]],
) -> Tuple[k8s_schemas.V1ObjectMeta, k8s_schemas.V1PodSpec]:
    if not main_container:
        raise PolypodException("A main container is required")
    environment = environment or V1Environment()

    metadata = k8s_schemas.V1ObjectMeta(
        name=resource_name,
        namespace=namespace,
        labels=labels,
        annotations=environment.annotations,
    )

    init_containers = to_list(init_containers, check_none=True)
    containers = [main_container] + to_list(sidecar_containers, check_none=True)
    image_pull_secrets = None
    if environment.image_pull_secrets:
        image_pull_secrets = [
            k8s_schemas.V1LocalObjectReference(name=i)
            for i in environment.image_pull_secrets
        ]

    pod_spec = k8s_schemas.V1PodSpec(
        init_containers=init_containers,
        containers=containers,
        volumes=volumes,
        restart_policy=environment.restart_policy,
        image_pull_secrets=image_pull_secrets,
        security_context=environment.security_context,
        service_account_name=environment.service_account_name,
        node_selector=environment.node_selector,
        tolerations=environment.tolerations,
        affinity=environment.affinity,
        dns_config=environment.dns_config,
        dns_policy=environment.dns_policy,
        host_aliases=environment.host_aliases,
        host_network=environment.host_network,
        node_name=environment.node_name,
        priority=environment.priority,
        priority_class_name=environment.priority_class_name,
        scheduler_name=environment.scheduler_name,
    )
    return metadata, pod_spec


def get_pod_template_spec(
    metadata: k8s_schemas.V1ObjectMeta, pod_spec: k8s_schemas.V1PodSpec
) -> k8s_schemas.V1PodTemplateSpec:
    return k8s_schemas.V1PodTemplateSpec(metadata=metadata, spec=pod_spec)
