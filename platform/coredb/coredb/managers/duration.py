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

from django.utils.timezone import now

from coredb.abstracts.runs import BaseRun
from polyaxon.lifecycle import LifeCycle


def set_started_at(run: BaseRun) -> bool:
    # We allow to override started_at if the value is running
    if run.started_at is not None:
        return False

    if LifeCycle.is_running(run.status):
        run.started_at = now()
        return True

    return False


def set_finished_at(run: BaseRun) -> bool:
    if LifeCycle.is_done(run.status) and run.finished_at is None:
        run.finished_at = now()
        if run.started_at is None:  # We should not have this case
            run.started_at = run.created_at
        # Update duration
        if run.duration is None:
            run.duration = (run.finished_at - run.started_at).seconds
        return True
    return False
