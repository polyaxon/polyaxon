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

import requests

import mock

from tests.test_transports.utils import BaseTestCaseTransport

from polyaxon.client.transport import Transport
from polyaxon.client.transport.utils import Bar


class TestHttpTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super().setUp()
        self.transport = Transport()

    def test_create_progress_callback(self):
        encoder = mock.MagicMock()
        encoder.configure_mock(len=10)
        _, progress_bar = self.transport.create_progress_callback(encoder)
        assert isinstance(progress_bar, Bar)

    def test_format_sizeof(self):
        assert self.transport.format_sizeof(10) == "10.0B"
        assert self.transport.format_sizeof(10000) == "9.8KiB"
        assert self.transport.format_sizeof(100000) == "97.7KiB"
        assert self.transport.format_sizeof(10000000) == "9.5MiB"
        assert self.transport.format_sizeof(10000000000) == "9.3GiB"

    def test_session(self):
        assert hasattr(self.transport, "_session") is False
        assert isinstance(self.transport.session, requests.Session)
        assert isinstance(self.transport._session, requests.Session)
