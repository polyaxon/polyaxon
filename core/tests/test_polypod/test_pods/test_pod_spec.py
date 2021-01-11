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

import pytest

from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.environment import V1Environment
from polyaxon.polypod.pod.spec import get_pod_spec
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestPodSpec(BaseTestCase):
    def test_get_pod_spec(self):
        init_container = k8s_schemas.V1Container(name="init")
        main_container = k8s_schemas.V1Container(name="main")
        sidecar_container = k8s_schemas.V1Container(name="sidecar")
        volumes = [k8s_schemas.V1Volume(name="vol")]
        labels = {"key": "labels"}
        annotations = {"key": "annotations"}
        node_selector = {"key": "selector"}
        affinity = [{"key": "affinity"}]
        tolerations = {"key": "tolerations"}
        security_context = {"uid": 222, "gid": 222}
        restart_policy = "never"

        with self.assertRaises(PolypodException):
            get_pod_spec(
                namespace="default",
                main_container=None,
                sidecar_containers=None,
                init_containers=None,
                resource_name="foo",
                volumes=None,
                environment=V1Environment(),
                labels={},
            )

        environment = V1Environment(
            service_account_name="sa",
            labels=labels,
            annotations=annotations,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            security_context=security_context,
            image_pull_secrets=[],
            restart_policy=restart_policy,
        )
        metadata, pod_spec = get_pod_spec(
            namespace="default",
            resource_name="foo",
            main_container=main_container,
            sidecar_containers=None,
            init_containers=None,
            volumes=None,
            environment=environment,
            labels=environment.labels,
        )

        assert metadata.name == "foo"
        assert metadata.labels == labels
        assert metadata.namespace == "default"
        assert metadata.annotations == annotations

        assert isinstance(pod_spec, k8s_schemas.V1PodSpec)
        assert pod_spec.security_context == security_context
        assert pod_spec.restart_policy == "never"
        assert pod_spec.service_account_name == "sa"
        assert pod_spec.init_containers == []
        assert pod_spec.containers == [main_container]
        assert pod_spec.volumes is None
        assert pod_spec.node_selector == node_selector
        assert pod_spec.tolerations == tolerations
        assert pod_spec.affinity == affinity

        environment = V1Environment(
            service_account_name="sa",
            labels=labels,
            annotations=annotations,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            security_context=security_context,
            image_pull_secrets=[],
            restart_policy=restart_policy,
        )
        metadata, pod_spec = get_pod_spec(
            namespace="default",
            main_container=main_container,
            sidecar_containers=[sidecar_container],
            init_containers=[init_container],
            resource_name="foo",
            volumes=volumes,
            environment=environment,
            labels={},
        )

        assert pod_spec.init_containers == [init_container]
        assert pod_spec.containers == [main_container, sidecar_container]
        assert pod_spec.volumes == volumes
        assert metadata.labels == {}
