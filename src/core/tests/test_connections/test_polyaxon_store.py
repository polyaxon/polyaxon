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

from mock import patch

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.stores.polyaxon_store import PolyaxonStore
from tests.utils import BaseTestCase


class TestPolyaxonStore(BaseTestCase):
    def test_download_file(self):
        store = PolyaxonStore(
            client=RunClient(owner="test", project="test", run_uuid="uid")
        )
        with patch(
            "polyaxon.stores.polyaxon_store.PolyaxonStore.download"
        ) as mock_call:
            result = store.download_file(url="url", path="test/path")

        assert result == "{}/uid/test/path".format(settings.CLIENT_CONFIG.archive_root)
        assert mock_call.call_count == 1
        assert mock_call.call_args_list[0][1] == {
            "filename": result,
            "params": {"path": "test/path"},
            "url": "url",
        }

        with patch(
            "polyaxon.stores.polyaxon_store.PolyaxonStore.download"
        ) as mock_call:
            result = store.download_file(url="url", path="test/path", untar=False)

        assert result == "{}/uid/test/path.tar.gz".format(
            settings.CLIENT_CONFIG.archive_root
        )
        assert mock_call.call_count == 1
        assert mock_call.call_args_list[0][1] == {
            "filename": result,
            "untar": False,
            "params": {"path": "test/path"},
            "url": "url",
        }

        with patch(
            "polyaxon.stores.polyaxon_store.PolyaxonStore.download"
        ) as mock_call:
            result = store.download_file(url="url", path="test/path", untar=True)

        assert result == "{}/uid/test/path".format(settings.CLIENT_CONFIG.archive_root)
        assert mock_call.call_count == 1
        assert mock_call.call_args_list[0][1] == {
            "filename": "{}.tar.gz".format(result),
            "untar": True,
            "params": {"path": "test/path"},
            "url": "url",
        }
