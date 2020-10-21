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

from polyaxon import settings
from polyaxon.streams.app.main import STREAMS_URL
from polyaxon.utils.path_utils import create_path
from tests.test_streams.base import create_tmp_files, get_streams_client, set_store
from tests.utils import BaseTestCase


class TestArtifactsEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.store_root = set_store()
        self.run_path = os.path.join(self.store_root, "uuid")
        # Create run artifacts path and some files
        create_path(self.run_path)
        create_tmp_files(self.run_path)

        self.client = get_streams_client()
        self.base_url = STREAMS_URL + "/namespace/owner/project/runs/uuid/artifacts"

    def test_download_artifacts(self):
        filepath = os.path.join(settings.CLIENT_CONFIG.archive_root, "uuid.tar.gz")
        assert os.path.exists(filepath) is False
        response = self.client.get(self.base_url)
        assert response.status_code == 200
        assert os.path.exists(filepath) is True
        assert response.headers["Content-Type"] == ""
        assert response.headers["X-Accel-Redirect"] == filepath
        assert response.headers[
            "Content-Disposition"
        ] == 'attachment; filename="{}"'.format("uuid.tar.gz")

    def test_delete_artifacts(self):
        # Created nested path
        nested_path = os.path.join(self.run_path, "foo")
        create_path(nested_path)
        create_tmp_files(nested_path)
        subpath = os.path.join(self.run_path, "foo")

        assert os.path.exists(self.run_path) is True
        assert os.path.exists(subpath) is True
        response = self.client.delete(self.base_url + "?path=foo")
        assert response.status_code == 204
        assert os.path.exists(self.run_path) is True
        assert os.path.exists(subpath) is False

        response = self.client.delete(self.base_url)
        assert response.status_code == 204
        assert os.path.exists(self.run_path) is False
