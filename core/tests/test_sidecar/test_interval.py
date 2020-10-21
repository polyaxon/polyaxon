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


from polyaxon.sidecar.intervals import get_sync_interval
from tests.utils import BaseTestCase


class TestSidecar(BaseTestCase):
    def test_get_interval_counter(self):
        assert get_sync_interval(0, 0) == -1
        assert get_sync_interval(1, 2) == 0
        assert get_sync_interval(2, 2) == 2
        assert get_sync_interval(3, 2) == 2
        assert get_sync_interval(4, 2) == 3
        assert get_sync_interval(4, 2) == 3
        assert get_sync_interval(6, 2) == 4
