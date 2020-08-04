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


from polyaxon.k8s.events import get_container_status, get_container_statuses_by_name
from polyaxon.k8s.pods import PodLifeCycle


def is_container_terminated(status, container_id):
    container_statuses = status.get("container_statuses") or []
    statuses_by_name = get_container_statuses_by_name(container_statuses)
    statuses = get_container_status(statuses_by_name, (container_id,))
    statuses = statuses or {}
    return statuses.get("state", {}).get("terminated")


def is_pod_running(event, container_id):
    event = event.to_dict()
    event_status = event.get("status", {})
    is_terminated = is_container_terminated(
        status=event_status, container_id=container_id
    )

    return (
        event_status.get("phase")
        in {PodLifeCycle.RUNNING, PodLifeCycle.PENDING, PodLifeCycle.CONTAINER_CREATING}
        and not is_terminated
    )
