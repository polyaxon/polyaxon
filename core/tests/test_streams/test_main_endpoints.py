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

from starlette.exceptions import HTTPException

from tests.test_streams.base import get_streams_client, set_store
from tests.utils import BaseTestCase


class TestMainEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        set_store()
        self.client = get_streams_client()

    def test_index_404(self):
        response = self.client.get("/")
        assert response.status_code == 404

    def test_404_page(self):
        response = self.client.get("/404")
        assert response.status_code == 404

    def test_500_page(self):
        with self.assertRaises(HTTPException):
            self.client.get("/500")

    def test_health_page(self):
        response = self.client.get("/healthz")
        assert response.status_code == 200
