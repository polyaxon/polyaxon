#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from django.db import transaction

from polycommon.celeryp.app import app
from polycommon.celeryp.polyaxon_task import PolyaxonTask

app.Task = PolyaxonTask  # Custom base class for logging


def send(task_name, kwargs=None, **options):
    options["ignore_result"] = options.get("ignore_result", True)
    return transaction.on_commit(
        lambda: app.send_task(task_name, kwargs=kwargs, **options)
    )
    # if "countdown" not in options:
    #     options["countdown"] = conf.get(SCHEDULER_GLOBAL_COUNTDOWN)
    # return app.send_task(task_name, kwargs=kwargs, **options)
