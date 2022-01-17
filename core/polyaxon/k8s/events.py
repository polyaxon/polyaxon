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


def get_container_statuses_by_name(statuses):
    return {
        container_status["name"]: {
            "ready": container_status["ready"],
            "state": container_status["state"],
        }
        for container_status in statuses
    }


def get_container_status(statuses, container_ids):
    job_container_status = None
    for container_id in container_ids:
        job_container_status = statuses.get(container_id)
        if job_container_status:
            break
    return job_container_status
