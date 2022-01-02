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

from polyaxon.client.transport import Transport
from polyaxon.schemas.cli.client_config import ClientConfig
from polyaxon.services.auth import AuthenticationTypes
from tests.test_transports.utils import BaseTestCaseTransport


class TestTransport(BaseTestCaseTransport):
    # pylint:disable=protected-access
    def setUp(self):
        super().setUp()
        self.transport = Transport()

    def test_get_headers(self):
        assert self.transport._get_headers() == {}
        assert self.transport._get_headers({"foo": "bar"}) == {"foo": "bar"}

        self.transport.config = ClientConfig(token="token", host="host")

        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format(AuthenticationTypes.TOKEN, "token")
        }
        assert self.transport._get_headers({"foo": "bar"}) == {
            "foo": "bar",
            "Authorization": "{} {}".format(AuthenticationTypes.TOKEN, "token"),
        }

        self.transport.config.authentication_type = AuthenticationTypes.INTERNAL_TOKEN
        assert self.transport._get_headers() == {
            "Authorization": "{} {}".format(AuthenticationTypes.INTERNAL_TOKEN, "token")
        }
        assert self.transport._get_headers({"foo": "bar"}) == {
            "foo": "bar",
            "Authorization": "{} {}".format(
                AuthenticationTypes.INTERNAL_TOKEN, "token"
            ),
        }
