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

from unittest import TestCase

from polycommon.events.registry import run


class TestEventsRegistry(TestCase):
    def _asser_event(self, event, value, expected, event_set):
        assert value == expected
        event_set.add(event.event_type)

    def test_events_subjects_runs(self):
        events = set([])
        self._asser_event(
            run.RunCreatedEvent, run.RunCreatedEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunCreatedActorEvent,
            run.RunCreatedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunUpdatedActorEvent,
            run.RunUpdatedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunViewedActorEvent,
            run.RunViewedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunStoppedEvent, run.RunStoppedEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunNewStatusEvent,
            run.RunNewStatusEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunNewArtifactsEvent,
            run.RunNewArtifactsEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunSucceededEvent,
            run.RunSucceededEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunResumedEvent, run.RunResumedEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunFailedEvent, run.RunFailedEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunDoneEvent, run.RunDoneEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunSkippedEvent, run.RunSkippedEvent.get_event_subject(), "run", events
        )
        self._asser_event(
            run.RunDeletedActorEvent,
            run.RunDeletedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunStoppedActorEvent,
            run.RunStoppedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunApprovedActorEvent,
            run.RunApprovedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunTransferredActorEvent,
            run.RunTransferredActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunResumedActorEvent,
            run.RunResumedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunRestartedActorEvent,
            run.RunRestartedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunCopiedActorEvent,
            run.RunCopiedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunSyncedActorEvent,
            run.RunSyncedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunSkippedActorEvent,
            run.RunSkippedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunInvalidatedActorEvent,
            run.RunInvalidatedActorEvent.get_event_subject(),
            "run",
            events,
        )
        self._asser_event(
            run.RunStatsActorEvent,
            run.RunStatsActorEvent.get_event_subject(),
            "run",
            events,
        )
        assert events == run.EVENTS

    def test_events_actions_runs(self):
        events = set([])
        self._asser_event(
            run.RunCreatedEvent, run.RunCreatedEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunStoppedEvent, run.RunStoppedEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunSkippedEvent, run.RunSkippedEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunResumedEvent, run.RunResumedEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunNewStatusEvent,
            run.RunNewStatusEvent.get_event_action(),
            None,
            events,
        )
        self._asser_event(
            run.RunNewArtifactsEvent,
            run.RunNewArtifactsEvent.get_event_action(),
            None,
            events,
        )
        self._asser_event(
            run.RunSucceededEvent,
            run.RunSucceededEvent.get_event_action(),
            None,
            events,
        )
        self._asser_event(
            run.RunFailedEvent, run.RunFailedEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunDoneEvent, run.RunDoneEvent.get_event_action(), None, events
        )
        self._asser_event(
            run.RunViewedActorEvent,
            run.RunViewedActorEvent.get_event_action(),
            "viewed",
            events,
        )
        self._asser_event(
            run.RunCreatedActorEvent,
            run.RunCreatedActorEvent.get_event_action(),
            "created",
            events,
        )
        self._asser_event(
            run.RunUpdatedActorEvent,
            run.RunUpdatedActorEvent.get_event_action(),
            "updated",
            events,
        )
        self._asser_event(
            run.RunDeletedActorEvent,
            run.RunDeletedActorEvent.get_event_action(),
            "deleted",
            events,
        )
        self._asser_event(
            run.RunStoppedActorEvent,
            run.RunStoppedActorEvent.get_event_action(),
            "stopped",
            events,
        )
        self._asser_event(
            run.RunApprovedActorEvent,
            run.RunApprovedActorEvent.get_event_action(),
            "approved",
            events,
        )
        self._asser_event(
            run.RunTransferredActorEvent,
            run.RunTransferredActorEvent.get_event_action(),
            "transferred",
            events,
        )
        self._asser_event(
            run.RunResumedActorEvent,
            run.RunResumedActorEvent.get_event_action(),
            "resumed",
            events,
        )
        self._asser_event(
            run.RunRestartedActorEvent,
            run.RunRestartedActorEvent.get_event_action(),
            "restarted",
            events,
        )
        self._asser_event(
            run.RunCopiedActorEvent,
            run.RunCopiedActorEvent.get_event_action(),
            "copied",
            events,
        )
        self._asser_event(
            run.RunSyncedActorEvent,
            run.RunSyncedActorEvent.get_event_action(),
            "synced",
            events,
        )
        self._asser_event(
            run.RunSkippedActorEvent,
            run.RunSkippedActorEvent.get_event_action(),
            "skipped",
            events,
        )
        self._asser_event(
            run.RunInvalidatedActorEvent,
            run.RunInvalidatedActorEvent.get_event_action(),
            "invalidated",
            events,
        )
        self._asser_event(
            run.RunStatsActorEvent,
            run.RunStatsActorEvent.get_event_action(),
            "stats",
            events,
        )
        assert events == run.EVENTS
