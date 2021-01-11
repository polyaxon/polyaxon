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

import os

from azure.storage.blob import BlobServiceClient

from polyaxon.connections.azure.azure_blobstore import get_blob_service_connection
from polyaxon.exceptions import PolyaxonConnectionError
from tests.utils import BaseTestCase


class TestAzureClient(BaseTestCase):
    def test_get_blob_service_connection(self):
        with self.assertRaises(PolyaxonConnectionError):
            get_blob_service_connection()

        service = get_blob_service_connection(account_name="foo", account_key="bar")
        assert isinstance(service, BlobServiceClient)

        os.environ["AZURE_ACCOUNT_NAME"] = "foo"
        os.environ["AZURE_ACCOUNT_KEY"] = "bar"
        service = get_blob_service_connection()
        assert isinstance(service, BlobServiceClient)
