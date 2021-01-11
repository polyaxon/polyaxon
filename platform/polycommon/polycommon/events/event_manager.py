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

from typing import List, Tuple

from polyaxon.utils.manager_interface import ManagerInterface
from polycommon.events import event_actions
from polycommon.events.event import Event


class EventManager(ManagerInterface):
    def _get_state_data(  # pylint:disable=arguments-differ
        self, event: Event
    ) -> Tuple[str, Event]:
        return event.event_type, event

    def subscribe(self, event: Event) -> None:  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeEvent)
        """
        super().subscribe(obj=event)

    def knows(self, event_type: str) -> bool:  # pylint:disable=arguments-differ
        return super().knows(key=event_type)

    def get(self, event_type: str) -> Event:  # pylint:disable=arguments-differ
        return super().get(key=event_type)

    def user_write_events(self) -> List[str]:
        """Return event types where use acted on an object.

        The write events are events with actions:
            * CREATED
            * UPDATED
            * DELETED
            * RESUMED
            * COPIED
            * CLONED
            * STOPPED
        """
        return [
            event_type
            for event_type, event in self.items
            if event.get_event_action() in event_actions.WRITE_ACTIONS
        ]

    def user_view_events(self) -> List[str]:
        """Return event types where use viewed a main object."""
        return [
            event_type
            for event_type, event in self.items
            if event.get_event_action() == event_actions.VIEWED
        ]
