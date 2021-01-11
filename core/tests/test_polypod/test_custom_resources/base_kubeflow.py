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
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.pod.spec import get_pod_spec, get_pod_template_spec
from polyaxon.polypod.specs.replica import ReplicaSpec
from tests.utils import BaseTestCase


class BaseKubeflowCRDTestCase(BaseTestCase):
    def get_replica(self, environment):
        main_container = k8s_schemas.V1Container(name="main")
        sidecar_containers = [k8s_schemas.V1Container(name="sidecar")]
        init_containers = [k8s_schemas.V1Container(name="init")]
        replica = ReplicaSpec(
            volumes=[],
            init_containers=init_containers,
            sidecar_containers=sidecar_containers,
            main_container=main_container,
            labels=environment.labels,
            environment=environment,
            num_replicas=12,
        )
        metadata, pod_spec = get_pod_spec(
            namespace="default",
            main_container=main_container,
            sidecar_containers=sidecar_containers,
            init_containers=init_containers,
            resource_name="foo",
            volumes=[],
            environment=environment,
            labels=environment.labels,
        )
        replica_template = {
            "replicas": replica.num_replicas,
            "restartPolicy": pod_spec.restart_policy,
            "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec),
        }
        return replica, replica_template
