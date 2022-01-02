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

from polyaxon.env_vars.getters.queue import get_queue_info
from polyaxon.exceptions import PolyaxonSchemaError
from tests.utils import BaseTestCase


class TestQueueEnvVars(BaseTestCase):
    def test_get_queue_info(self):
        with self.assertRaises(PolyaxonSchemaError):
            get_queue_info(None)

        with self.assertRaises(PolyaxonSchemaError):
            get_queue_info("")

        with self.assertRaises(PolyaxonSchemaError):
            get_queue_info("foo/bar/noo")

        with self.assertRaises(PolyaxonSchemaError):
            get_queue_info("foo.bar.noo")

        assert get_queue_info("test") == (None, "test")
        assert get_queue_info("agent.queue") == ("agent", "queue")
        assert get_queue_info("agent/queue") == ("agent", "queue")
