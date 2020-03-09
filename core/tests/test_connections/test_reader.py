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

import os

from tests.utils import BaseTestCase

from polyaxon.connections.reader import get_from_env


class TestReader(BaseTestCase):
    def test_get_from_env(self):
        assert get_from_env(keys=None) is None
        assert get_from_env(keys=[]) is None
        assert get_from_env(keys="some_random_text_foo_000") is None

        os.environ["some_random_text_foo_000"] = "a"

        assert get_from_env(["some_random_text_foo_000"]) == "a"

        del os.environ["some_random_text_foo_000"]

        os.environ["POLYAXON_some_random_text_foo_000"] = "a"

        assert get_from_env(["some_random_text_foo_000"]) == "a"

        del os.environ["POLYAXON_some_random_text_foo_000"]
