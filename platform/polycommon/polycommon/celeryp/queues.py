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


class CeleryCoreQueues:
    """Celery Core Queues.

    N.B. make sure that the queue name is not < 128.
    """

    SCHEDULER_HEALTH = "queues.scheduler.health"
    SCHEDULER_RUNS = "queues.scheduler.runs"
    SCHEDULER_COMPILER = "queues.scheduler.compiler"
    SCHEDULER_ARTIFACTS = "queues.scheduler.artifacts"
    SCHEDULER_CLEAN = "queues.scheduler.clean"
