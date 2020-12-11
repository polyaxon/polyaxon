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


class CoreSchedulerCeleryTasks:
    """Scheduler celery tasks.

    N.B. make sure that the task name is not < 128.
    """

    SCHEDULER_HEALTH = "scheduler_health"

    RUNS_PREPARE = "runs_prepare"
    RUNS_START = "runs_start"
    RUNS_STOP = "runs_stop"
    RUNS_DELETE = "runs_delete"
    RUNS_SET_ARTIFACTS = "runs_set_artifacts"
