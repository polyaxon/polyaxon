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

from polycommon.checks import health_task
from polycommon.celeryp.tasks import CoreSchedulerCeleryTasks
from polycommon import workers


@workers.app.task(name=CoreSchedulerCeleryTasks.SCHEDULER_HEALTH, ignore_result=False)
def scheduler_health(x, y):
    return health_task.health_task(x, y)
