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

import mock

from tests.utils import BaseTestCase

from polyaxon.connections.gcp.base import get_gc_client, get_gc_credentials
from polyaxon.exceptions import PolyaxonStoresException

GCS_MODULE = "polyaxon.connections.gcp.base.{}"


class TestGCClient(BaseTestCase):
    @mock.patch(GCS_MODULE.format("google.auth.default"))
    def test_get_default_gc_credentials(self, default_auth):
        default_auth.return_value = None, None
        credentials = get_gc_credentials()
        assert default_auth.call_count == 1
        assert credentials is None

    @mock.patch(GCS_MODULE.format("Credentials.from_service_account_file"))
    def test_get_key_path_gc_credentials(self, service_account):

        with self.assertRaises(PolyaxonStoresException):
            get_gc_credentials(key_path="key_path")

        service_account.return_value = None
        credentials = get_gc_credentials(key_path="key_path.json")
        assert service_account.call_count == 1
        assert credentials is None

    @mock.patch(GCS_MODULE.format("Credentials.from_service_account_info"))
    def test_get_keyfile_dict_gc_credentials(self, service_account):
        with self.assertRaises(PolyaxonStoresException):
            get_gc_credentials(keyfile_dict="keyfile_dict")

        service_account.return_value = None

        credentials = get_gc_credentials(keyfile_dict={"private_key": "key"})
        assert service_account.call_count == 1
        assert credentials is None

        credentials = get_gc_credentials(keyfile_dict='{"private_key": "private_key"}')
        assert service_account.call_count == 2
        assert credentials is None

    @mock.patch(GCS_MODULE.format("get_gc_credentials"))
    @mock.patch(GCS_MODULE.format("Client"))
    def test_get_gc_client(self, client, gc_credentials):
        get_gc_client()
        assert gc_credentials.call_count == 1
        assert client.call_count == 1
