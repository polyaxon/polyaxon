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

from coredb.executor.handlers import run as run_handlers
from coredb.executor.manager import event_manager
from polyaxon.utils.imports import import_string
from polycommon.events.event_service import EventService
from polycommon.events.registry import run


class ExecutorService(EventService):
    HANDLER_MAPPING = {
        run.RUN_CREATED: run_handlers.handle_run_created,
        run.RUN_RESUMED_ACTOR: run_handlers.handle_run_created,
        run.RUN_CLEANED: run_handlers.handle_run_cleaned_triggered,
        run.RUN_STOPPED_ACTOR: run_handlers.handle_run_stopped_triggered,
    }

    event_manager = event_manager

    def __init__(self, workers_service=None):
        self.workers_service = workers_service
        self.workers = None

    def record_event(self, event: "Event") -> None:  # noqa: F821
        if self.workers and event.event_type in self.HANDLER_MAPPING:
            self.HANDLER_MAPPING[event.event_type](
                workers_backend=self.workers, event=event
            )

    def setup(self) -> None:
        super().setup()
        # Load default event types
        import coredb.executor.subscriptions  # noqa

        if self.workers_service:
            self.workers = import_string(self.workers_service)
