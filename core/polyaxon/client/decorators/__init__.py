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
from polyaxon.client.decorators.can_log_event import can_log_events
from polyaxon.client.decorators.can_log_outputs import can_log_outputs
from polyaxon.client.decorators.is_managed import ensure_is_managed
from polyaxon.client.decorators.no_op import check_no_op
from polyaxon.client.decorators.offline import check_offline
