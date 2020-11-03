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
from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.custom_resources.crd import get_custom_object
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow import V1Notification
from polyaxon.polyflow.environment import V1Environment
from polyaxon.polyflow.termination import V1Termination
from polyaxon.polypod.custom_resources import get_job_custom_resource
from polyaxon.polypod.pod.spec import get_pod_spec, get_pod_template_spec
from tests.utils import BaseTestCase


class TestJobCRD(BaseTestCase):
    def test_get_job_custom_resource(self):
        main_container = k8s_schemas.V1Container(name="main")
        sidecar_containers = [k8s_schemas.V1Container(name="sidecar")]
        init_containers = [k8s_schemas.V1Container(name="init")]
        termination = V1Termination(max_retries=5, ttl=10, timeout=10)
        environment = V1Environment(
            labels={"foo": "bar"},
            annotations={"foo": "bar"},
            node_selector={"foo": "bar"},
            node_name="foo",
            restart_policy="never",
        )
        notifications = [V1Notification(connections=["test"], trigger=V1Statuses.DONE)]
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
        custom_object = {
            "batchJobSpec": {
                "template": get_pod_template_spec(metadata=metadata, pod_spec=pod_spec),
            },
            "termination": {
                "backoffLimit": termination.max_retries,
                "activeDeadlineSeconds": termination.timeout,
                "ttlSecondsAfterFinished": termination.ttl,
            },
            "collectLogs": True,
            "syncStatuses": True,
            "notifications": [n.to_operator() for n in notifications],
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

        crd = get_job_custom_resource(
            namespace="default",
            resource_name="foo",
            main_container=main_container,
            sidecar_containers=sidecar_containers,
            init_containers=init_containers,
            volumes=[],
            termination=termination,
            environment=environment,
            collect_logs=True,
            sync_statuses=True,
            notifications=notifications,
            labels=environment.labels,
            annotations={"foo": "long-foo-bar" * 300},
        )

        assert crd == expected_crd
