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

import pytest

from polyaxon.polyboard.processors.events_processors import metrics_dict_to_list
from tests.utils import BaseTestCase


@pytest.mark.tracking_mark
class TestEventWriter(BaseTestCase):
    def test_gpu_resources_to_metrics(self):
        resources = {
            "gpu_0_memory_free": 1000,
            "gpu_0_memory_used": 8388608000,
            "gpu_0_utilization": 76,
        }

        events = metrics_dict_to_list(resources)
        assert len(events) == 3
        assert [e.event.metric for e in events] == [1000, 8388608000, 76]

    def test_psutil_resources_to_metrics(self):
        resources = {
            "cpu_percent_avg": 1000,
            "cpu_percent_1": 0.3,
            "cpu_percent_2": 0.5,
            "getloadavg": 76,
            "memory_total": 12883853312,
            "memory_used": 8388608000,
        }

        events = metrics_dict_to_list(resources)
        assert len(events) == 6
        assert [e.event.metric for e in events] == [
            1000,
            0.3,
            0.5,
            76,
            12883853312,
            8388608000,
        ]
