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

import logging

from celery import Task

_logger = logging.getLogger("polyaxon.tasks")


class PolyaxonTask(Task):
    """Base custom celery task with basic logging."""

    abstract = True

    def on_success(self, retval, task_id, args, kwargs):
        _logger.info("Async task succeeded", extra={"task name": self.name})

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        extra = {
            "task name": self.name,
            "task id": task_id,
            "task args": args,
            "task kwargs": kwargs,
        }
        _logger.error("Async Task Failed", exc_info=einfo, extra=extra)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        _logger.info("Async task retry", extra={"task name": self.name})
