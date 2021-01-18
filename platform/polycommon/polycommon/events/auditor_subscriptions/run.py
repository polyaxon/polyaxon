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

from polycommon import auditor
from polycommon.events.registry import run

auditor.subscribe(run.RunCreatedEvent)
auditor.subscribe(run.RunResumedEvent)
auditor.subscribe(run.RunStoppedEvent)
auditor.subscribe(run.RunSkippedEvent)
auditor.subscribe(run.RunNewStatusEvent)
auditor.subscribe(run.RunNewArtifactsEvent)
auditor.subscribe(run.RunSucceededEvent)
auditor.subscribe(run.RunFailedEvent)
auditor.subscribe(run.RunDoneEvent)
auditor.subscribe(run.RunCreatedActorEvent)
auditor.subscribe(run.RunUpdatedActorEvent)
auditor.subscribe(run.RunDeletedActorEvent)
auditor.subscribe(run.RunViewedActorEvent)
auditor.subscribe(run.RunStoppedActorEvent)
auditor.subscribe(run.RunApprovedActorEvent)
auditor.subscribe(run.RunInvalidatedActorEvent)
auditor.subscribe(run.RunResumedActorEvent)
auditor.subscribe(run.RunRestartedActorEvent)
auditor.subscribe(run.RunCopiedActorEvent)
auditor.subscribe(run.RunSkippedActorEvent)
auditor.subscribe(run.RunStatsActorEvent)
