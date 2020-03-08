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
import tempfile
import time

import mock

from azure.storage.blob import Blob, BlobPrefix, BlobProperties
from tests.utils import BaseTestCase

from polyaxon.connections.azure.azure_blobstore import AzureBlobStoreService
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.utils.date_utils import to_datetime

AZURE_MODULE = "polyaxon.connections.azure.azure_blobstore.{}"


class MockBlobList(object):
    def __init__(self, items, next_marker=None):
        self.items = items
        self.next_marker = next_marker

    def __iter__(self):
        return iter(self.items)


class TestAzureStore(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.wasbs_base = "wasbs://container@user.blob.core.windows.net/"

    def test_parse_wasbs_url(self):
        # Correct url
        wasbs_url = "wasbs://container@user.blob.core.windows.net/path"
        parsed_url = AzureBlobStoreService.parse_wasbs_url(wasbs_url)
        assert parsed_url == ("container", "user", "path")
        wasbs_url = "wasbs://container@user.blob.core.windows.net/"
        parsed_url = AzureBlobStoreService.parse_wasbs_url(wasbs_url)
        assert parsed_url == ("container", "user", "")
        wasbs_url = "wasbs://container@user.blob.core.windows.net"
        parsed_url = AzureBlobStoreService.parse_wasbs_url(wasbs_url)
        assert parsed_url == ("container", "user", "")
        wasbs_url = "wasbs://container@user.blob.core.windows.net/path/to/file"
        parsed_url = AzureBlobStoreService.parse_wasbs_url(wasbs_url)
        assert parsed_url == ("container", "user", "path/to/file")

        # Wrong url
        wasbs_url = "wasbs://container@user.foo.bar.windows.net/path/to/file"
        with self.assertRaises(PolyaxonStoresException):
            AzureBlobStoreService.parse_wasbs_url(wasbs_url)

        wasbs_url = "wasbs://container@user.blob.core.foo.net/path/to/file"
        with self.assertRaises(PolyaxonStoresException):
            AzureBlobStoreService.parse_wasbs_url(wasbs_url)

        wasbs_url = "wasbs://container@user.blob.windows.net/path/to/file"
        with self.assertRaises(PolyaxonStoresException):
            AzureBlobStoreService.parse_wasbs_url(wasbs_url)

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_list_empty(self, client):
        client.return_value.list_blobs.return_value = MockBlobList([])

        store = AzureBlobStoreService()
        key_path = self.wasbs_base + "path"
        assert store.list(key=key_path) == {"blobs": [], "prefixes": []}

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_list_non_empty(self, client):
        base_path = "/path/"
        # Create some files to return
        dir_prefix = BlobPrefix()
        dir_prefix.name = base_path + "dir"

        blob_props = BlobProperties()
        blob_props.content_length = 42
        blob = Blob(base_path + "file", props=blob_props)

        client.return_value.list_blobs.return_value = MockBlobList([dir_prefix, blob])

        store = AzureBlobStoreService()
        key_path = self.wasbs_base + base_path
        results = store.list(key=key_path)
        assert len(results["blobs"]) == 1
        assert len(results["prefixes"]) == 1
        assert results["prefixes"][0] == "dir"
        assert results["blobs"][0][0] == "file"
        assert results["blobs"][0][1] == 42

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_upload_file(self, client):
        dirname = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"
        open(fpath, "w")

        base_path = "path/"
        base_path_file = base_path + "test.txt"
        store = AzureBlobStoreService()

        # Test without basename
        key_path = self.wasbs_base + base_path_file
        store.upload_file(filename=fpath, blob=key_path, use_basename=False)
        client.return_value.create_blob_from_path.assert_called_with(
            "container", base_path_file, fpath
        )

        # Test with basename
        key_path = self.wasbs_base + base_path
        store.upload_file(filename=fpath, blob=key_path, use_basename=True)
        client.return_value.create_blob_from_path.assert_called_with(
            "container", base_path_file, fpath
        )

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_download_file(self, client):
        client.return_value.list_blobs.return_value = MockBlobList([])

        dirname = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"

        def mkfile(container, cloud_path, fname):
            return open(fname, "w")

        client.return_value.get_blob_to_path.side_effect = mkfile

        base_path = "path/test.txt"
        store = AzureBlobStoreService()
        key_path = self.wasbs_base + base_path

        # Test without basename
        store.download_file(key_path, fpath, use_basename=False)
        client.return_value.get_blob_to_path.assert_called_with(
            "container", base_path, fpath
        )

        # Test without basename
        store.download_file(key_path, dirname, use_basename=True)
        client.return_value.get_blob_to_path.assert_called_with(
            "container", base_path, fpath
        )

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_delete_file(self, client):
        client.return_value.list_blobs.return_value = MockBlobList([])

        base_path = "path/test.txt"
        store = AzureBlobStoreService()
        key_path = self.wasbs_base + base_path

        # Test without basename
        store.delete(key_path)
        client.return_value.delete_blob.assert_called_with("container", "path/test.txt")

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_upload_dir(self, client):
        dirname1 = tempfile.mkdtemp()
        fpath1 = dirname1 + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname1 + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        store = AzureBlobStoreService()

        blob_path = "path/to/"
        azure_url = self.wasbs_base + blob_path
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        store.upload_dir(dirname=dirname1, blob=azure_url, use_basename=False)
        client.return_value.create_blob_from_path.assert_has_calls(
            [
                mock.call("container", "{}test1.txt".format(blob_path), fpath1),
                mock.call("container", "{}test2.txt".format(blob_path), fpath2),
                mock.call(
                    "container", "{}{}/test3.txt".format(blob_path, rel_path2), fpath3
                ),
            ],
            any_order=True,
        )

        # Test with basename
        store.upload_dir(dirname=dirname1, blob=azure_url, use_basename=True)
        client.return_value.create_blob_from_path.assert_has_calls(
            [
                mock.call(
                    "container", "{}{}/test1.txt".format(blob_path, rel_path1), fpath1
                ),
                mock.call(
                    "container", "{}{}/test2.txt".format(blob_path, rel_path1), fpath2
                ),
                mock.call(
                    "container",
                    "{}{}/{}/test3.txt".format(blob_path, rel_path1, rel_path2),
                    fpath3,
                ),
            ],
            any_order=True,
        )

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_upload_dir_with_last_time(self, client):
        dirname1 = tempfile.mkdtemp()
        fpath1 = dirname1 + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname1 + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        last_time = to_datetime(os.stat(fpath2).st_mtime)
        time.sleep(0.1)

        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        store = AzureBlobStoreService()

        blob_path = "path/to/"
        azure_url = self.wasbs_base + blob_path
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        store.upload_dir(
            dirname=dirname1, blob=azure_url, use_basename=False, last_time=last_time
        )
        client.return_value.create_blob_from_path.assert_has_calls(
            [
                mock.call(
                    "container", "{}{}/test3.txt".format(blob_path, rel_path2), fpath3
                )
            ],
            any_order=True,
        )

        # Test with basename
        store.upload_dir(
            dirname=dirname1, blob=azure_url, use_basename=True, last_time=last_time
        )
        client.return_value.create_blob_from_path.assert_has_calls(
            [
                mock.call(
                    "container",
                    "{}{}/{}/test3.txt".format(blob_path, rel_path1, rel_path2),
                    fpath3,
                )
            ],
            any_order=True,
        )

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_download_dir(self, client):
        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        def mkfile(container, cloud_path, fname):
            return open(fname, "w")

        client.return_value.get_blob_to_path.side_effect = mkfile

        store = AzureBlobStoreService()

        blob_path = "/path/to/"
        azure_url = self.wasbs_base + blob_path
        rel_path2 = dirname2.split("/")[-1]

        # Mock return list
        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock1 = Blob(blob_path + "test1.txt", props=blob_props)

        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock2 = Blob(blob_path + "test2.txt", props=blob_props)

        subdir_mock = BlobPrefix()
        subdir_mock.name = blob_path + rel_path2

        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock3 = Blob(blob_path + rel_path2 + "/" + "test3.txt", props=blob_props)

        # Create some files to return
        def list_side_effect(container_name, prefix, delimiter="/", marker=None):
            if prefix == blob_path:
                return MockBlobList([subdir_mock, obj_mock1, obj_mock2])
            return MockBlobList([obj_mock3])

        client.return_value.list_blobs.side_effect = list_side_effect

        dirname3 = tempfile.mkdtemp()

        # Test without basename
        store.download_dir(blob=azure_url, local_path=dirname3, use_basename=False)
        client.return_value.get_blob_to_path.assert_has_calls(
            [
                mock.call(
                    "container",
                    "{}test1.txt".format(blob_path),
                    "{}/test1.txt".format(dirname3),
                ),
                mock.call(
                    "container",
                    "{}test2.txt".format(blob_path),
                    "{}/test2.txt".format(dirname3),
                ),
                mock.call(
                    "container",
                    "{}{}/test3.txt".format(blob_path, rel_path2),
                    "{}/{}/test3.txt".format(dirname3, rel_path2),
                ),
            ],
            any_order=True,
        )

    @mock.patch(AZURE_MODULE.format("BlockBlobService"))
    def test_download_dir_with_basename(self, client):
        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        def mkfile(container, cloud_path, fname):
            return open(fname, "w")

        client.return_value.get_blob_to_path.side_effect = mkfile

        store = AzureBlobStoreService()

        blob_path = "/path/to/"
        azure_url = self.wasbs_base + blob_path
        rel_path2 = dirname2.split("/")[-1]

        # Mock return list
        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock1 = Blob(blob_path + "foo/test1.txt", props=blob_props)

        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock2 = Blob(blob_path + "foo/test2.txt", props=blob_props)

        subdir_mock = BlobPrefix()
        subdir_mock.name = blob_path + "foo/" + rel_path2

        blob_props = BlobProperties()
        blob_props.content_length = 42
        obj_mock3 = Blob(
            blob_path + "foo/" + rel_path2 + "/" + "test3.txt", props=blob_props
        )

        # Create some files to return
        def list_side_effect(container_name, prefix, delimiter="/", marker=None):
            if prefix == blob_path + "foo/":
                return MockBlobList([subdir_mock, obj_mock1, obj_mock2])
            return MockBlobList([obj_mock3])

        client.return_value.list_blobs.side_effect = list_side_effect

        dirname3 = tempfile.mkdtemp()

        # Test without basename
        store.download_dir(
            blob=azure_url + "foo", local_path=dirname3, use_basename=True
        )
        client.return_value.get_blob_to_path.assert_has_calls(
            [
                mock.call(
                    "container",
                    "{}foo/test1.txt".format(blob_path),
                    "{}/foo/test1.txt".format(dirname3),
                ),
                mock.call(
                    "container",
                    "{}foo/test2.txt".format(blob_path),
                    "{}/foo/test2.txt".format(dirname3),
                ),
                mock.call(
                    "container",
                    "{}foo/{}/test3.txt".format(blob_path, rel_path2),
                    "{}/foo/{}/test3.txt".format(dirname3, rel_path2),
                ),
            ],
            any_order=True,
        )
