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
from polyaxon.k8s.custom_resources.crd import get_custom_object
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1Notification
from polyaxon.polyflow.environment import V1Environment
from polyaxon.polyflow.termination import V1Termination
from polyaxon.polypod.custom_resources import get_service_custom_resource
from polyaxon.polypod.pod.spec import get_pod_spec, get_pod_template_spec
from tests.utils import BaseTestCase


class TestServiceCRD(BaseTestCase):
    def test_get_service_custom_resource(self):
        main_container = k8s_schemas.V1Container(name="main")
        sidecar_containers = [k8s_schemas.V1Container(name="sidecar")]
        init_containers = [k8s_schemas.V1Container(name="init")]
        termination = V1Termination(timeout=10)
        environment = V1Environment(
            labels={"foo": "bar"},
            annotations={"foo": "long-foo-bar" * 300},
            node_selector={"foo": "bar"},
            node_name="foo",
            restart_policy="never",
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
            annotations=environment.annotations,
        )
        custom_object = {
            "serviceSpec": {
                "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec),
            },
            "termination": {"activeDeadlineSeconds": termination.timeout},
            "collectLogs": True,
            "syncStatuses": True,
            "notifications": [],
        }
        expected_crd = get_custom_object(
            namespace="default",
            resource_name="foo",
            kind="Operation",
            api_version="core.polyaxon.com/v1",
            labels={"foo": "bar"},
            custom_object=custom_object,
            annotations={"foo": "long-foo-bar" * 300},
        )

        crd = get_service_custom_resource(
            namespace="default",
            resource_name="foo",
            main_container=main_container,
            sidecar_containers=sidecar_containers,
            init_containers=init_containers,
            volumes=[],
            termination=termination,
            environment=environment,
            labels=environment.labels,
            annotations={"foo": "long-foo-bar" * 300},
            collect_logs=True,
            sync_statuses=True,
            notifications=None,
            ports=[],
        )

        assert crd == expected_crd

    def test_get_service_custom_resource_missing_keys(self):
        main_container = k8s_schemas.V1Container(name="main")
        metadata, pod_spec = get_pod_spec(
            namespace="default",
            main_container=main_container,
            sidecar_containers=None,
            init_containers=None,
            resource_name="foo",
            volumes=[],
            environment=None,
            labels=None,
            annotations=None,
        )
        notifications = [V1Notification(connections=["test"], trigger=V1Statuses.DONE)]
        custom_object = {
            "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec),
            "ports": [12, 121, 12],
        }
        expected_crd = get_custom_object(
            namespace="default",
            resource_name="foo",
            kind="Operation",
            api_version="core.polyaxon.com/v1",
            labels=None,
            annotations=None,
            custom_object={
                "serviceSpec": custom_object,
                "collectLogs": False,
                "syncStatuses": False,
                "notifications": [n.to_operator() for n in notifications],
            },
        )

        crd = get_service_custom_resource(
            namespace="default",
            resource_name="foo",
            main_container=main_container,
            sidecar_containers=None,
            init_containers=None,
            volumes=[],
            termination=None,
            collect_logs=None,
            sync_statuses=None,
            notifications=notifications,
            environment=None,
            labels=None,
            annotations=None,
            ports=[12, 121, 12],
        )

        assert crd == expected_crd
