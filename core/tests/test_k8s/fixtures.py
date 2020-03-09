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


def get_status_event(name, container_name, labels):
    event = {
        "type": "ADDED",
        "object": {
            "api_version": "v1",
            "kind": "Pod",
            "metadata": {
                "deletion_timestamp": None,
                "name": name,
                "namespace": "polyaxon",
                "owner_references": None,
                "resource_version": "277329",
                "self_link": "/api/v1/namespaces/polyaxon/pods/project1-id1-spec1-xp1-master0",
                "uid": "05062d42-d915-11e7-8ab8-1273d6911587",
                "labels": labels,
            },
            "spec": {
                "containers": [
                    {
                        "command": ["python3", "-c"],
                        "env": [],
                        "image": "busybox/busybox",
                        "image_pull_policy": "IfNotPresent",
                        "lifecycle": None,
                        "liveness_probe": None,
                        "name": container_name,
                        "ports": [
                            {
                                "container_port": 2222,
                                "host_ip": None,
                                "host_port": None,
                                "name": None,
                                "protocol": "TCP",
                            }
                        ],
                        "readiness_probe": None,
                    }
                ],
                "volumes": [],
                "node_name": None,
            },
            "status": {
                "conditions": None,
                "container_statuses": None,
                "host_ip": None,
                "init_container_statuses": None,
                "message": None,
                "phase": "Pending",
                "pod_ip": None,
                "qos_class": "BestEffort",
                "reason": None,
                "start_time": None,
            },
        },
    }
    return event


def get_status_event_with_conditions(name, container_name, labels):
    event = get_status_event(name, container_name, labels)
    event["object"]["status"] = {
        "conditions": [
            {
                "last_probe_time": None,
                "message": None,
                "reason": None,
                "status": "True",
                "type": "Initialized",
            },
            {
                "last_probe_time": None,
                "message": "containers with unready status: [{}]".format(
                    container_name
                ),
                "reason": "ContainersNotReady",
                "status": "False",
                "type": "Ready",
            },
            {
                "last_probe_time": None,
                "message": None,
                "reason": None,
                "status": "True",
                "type": "PodScheduled",
            },
        ],
        "container_statuses": [
            {
                "container_id": "docker://539e6a6f4209997094802b0657f90576fe129b7f81697120172836073d9bbd75",  # noqa
                "image": "busybox/busybox",
                "image_id": "docker://sha256:c66a51ffd71e2ec0cb0699dba06283bce9d254e2833a84ce7378298b04297ba3",  # noqa
                "last_state": {"running": None, "terminated": None, "waiting": None},
                "name": container_name,
                "ready": False,
                "restart_count": 0,
                "state": {
                    "running": 1,  # This is changed to get the test to check container monitoring
                    "terminated": {
                        "container_id": "docker://539e6a6f4209997094802b0657f90576fe129b7f81697120172836073d9bbd75",  # noqa
                        "exit_code": 1,
                        "message": None,
                        "reason": "Error",
                        "signal": None,
                    },
                    "waiting": None,
                },
            }
        ],
        "host_ip": "192.168.64.4",
        "init_container_statuses": None,
        "message": None,
        "phase": "Failed",
        "pod_ip": "172.17.0.2",
        "qos_class": "BestEffort",
        "reason": None,
    }
    return event


status_run_job_event = get_status_event(
    name="run1", container_name="polyaxon-main-job", labels={}
)

status_run_job_event_with_conditions = get_status_event_with_conditions(
    name="run1", container_name="polyaxon-main-job", labels={}
)
