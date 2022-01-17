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

import requests

from polyaxon.client.transport import Transport
from tests.test_transports.utils import BaseTestCaseTransport


class TestHttpTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super().setUp()
        self.transport = Transport()

    def test_session(self):
        assert hasattr(self.transport, "_session") is False
        assert isinstance(self.transport.session, requests.Session)
        assert isinstance(self.transport._session, requests.Session)
