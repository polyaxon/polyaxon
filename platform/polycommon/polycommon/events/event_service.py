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

from typing import Any, Mapping, Optional

from polycommon.events.event import Event
from polycommon.service_interface import Service


class EventService(Service):
    __all__ = ("record",)

    event_manager = None

    def can_handle(self, event_type: str) -> bool:
        return isinstance(event_type, str) and self.event_manager.knows(event_type)

    def get_event(
        self,
        event_type: str,
        event_data: Mapping = None,
        instance: Any = None,
        **kwargs
    ) -> Event:
        if instance or not event_data:
            return self.event_manager.get(event_type).from_instance(instance, **kwargs)
        return self.event_manager.get(event_type).from_event_data(
            event_data=event_data, **kwargs
        )

    def record(
        self,
        event_type: str,
        event_data: Mapping = None,
        instance: Any = None,
        **kwargs
    ) -> Optional[Event]:
        """Validate and record an event.

        >>> record('event.action', object_instance)
        """
        if not self.is_setup:
            return
        if not self.can_handle(event_type=event_type):
            return

        event = self.get_event(
            event_type=event_type, event_data=event_data, instance=instance, **kwargs
        )
        self.record_event(event)
        return event

    def record_event(self, event: Event) -> None:
        """Record an event.

        >>> record_event(Event())
        """
