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

import mock
import os
import tempfile
import time

from polyaxon.connections.gcp.gcs import GCSService
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.utils.date_utils import to_datetime
from tests.utils import BaseTestCase

GCP_BASE_MODULE = "polyaxon.connections.gcp.base.{}"
GCP_MODULE = "polyaxon.connections.gcp.service.{}"


class TestGCSStore(BaseTestCase):
    def test_parse_gcs_url(self):
        # Correct url
        gcs_url = "gs://bucket/path/to/blob"
        parsed_url = GCSService.parse_gcs_url(gcs_url)
        assert parsed_url == ("bucket", "path/to/blob")

        # Wrong url
        gcs_url = "gs:/bucket/path/to/blob"
        with self.assertRaises(PolyaxonStoresException):
            GCSService.parse_gcs_url(gcs_url)

        # Trailing slash
        gcs_url = "gs://bucket/path/to/blob/"
        assert GCSService.parse_gcs_url(gcs_url) == ("bucket", "path/to/blob/")

        # Bucket only
        gcs_url = "gs://bucket/"
        assert GCSService.parse_gcs_url(gcs_url) == ("bucket", "")

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_store_client(self, get_gc_client, gc_credentials):
        get_gc_client.return_value = "client"
        store = GCSService(connection="foo")
        assert store.connection == "foo"

        store = GCSService()
        assert store.connection == "client"
        assert gc_credentials.call_count == 0
        assert get_gc_client.call_count == 1

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_existing_object(self, get_gc_client, _):
        test_bucket = "test_bucket"
        test_object = "test_object"

        get_gc_client.return_value.objects.return_value.get.return_value.execute.return_value = {
            "kind": "storage#object",
            # the bucket name, object name, and generation number.
            "id": "{}/{}/1521132662504504".format(test_bucket, test_object),
            "name": test_object,
            "bucket": test_bucket,
            "generation": "1521132662504504",
            "contentType": "text/csv",
            "timeCreated": "2018-03-15T16:51:02.502Z",
            "updated": "2018-03-15T16:51:02.502Z",
            "storageClass": "MULTI_REGIONAL",
            "timeStorageClassUpdated": "2018-03-15T16:51:02.502Z",
            "size": "89",
            "md5Hash": "leYUJBUWrRtks1UeUFONJQ==",
            "metadata": {"md5-hash": "95e614241516ad1b64b3551e50538d25"},
            "crc32c": "xgdNfQ==",
            "etag": "CLf4hODk7tkCEAE=",
        }

        response = GCSService().check_blob(blob=test_object, bucket_name=test_bucket)
        assert response is True

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_non_existing_object(self, get_gc_client, _):
        test_bucket = "test_bucket"
        test_object = "test_object"

        get_gc_client.return_value.get_bucket.return_value.get_blob.side_effect = (
            Exception
        )

        response = GCSService().check_blob(blob=test_object, bucket_name=test_bucket)
        assert response is False

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_get_bucket(self, get_gc_client, _):
        test_bucket = "test_bucket"

        get_gc_client.return_value.get_bucket.return_value = {}

        response = GCSService().get_bucket(bucket_name=test_bucket)

        assert response == {}

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_get_blob(self, get_gc_client, _):
        test_bucket = "test_bucket"
        test_object = "test_object"

        bucket = mock.MagicMock()
        get_gc_client.return_value.get_bucket.return_value = bucket
        bucket.get_blob.return_value = {}

        response = GCSService().get_blob(blob=test_object, bucket_name=test_bucket)

        assert response == {}

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_delete(self, get_gc_client, _):
        test_bucket = "test_bucket"
        test_object = "test_object"

        # Correct file
        bucket = mock.MagicMock()
        get_gc_client.return_value.get_bucket.return_value = bucket
        bucket.delete_blob.return_value = True

        GCSService().delete(key=test_object, bucket_name=test_bucket)

        # Wrong file
        bucket = mock.MagicMock()
        get_gc_client.return_value.get_bucket.return_value = bucket
        bucket.delete_blob.return_value = True

        GCSService().delete(key=test_object, bucket_name=test_bucket)

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_list_empty(self, get_gc_client, _):
        gcs_url = "gs://bucket/path/to/blob"
        store = GCSService()
        assert store.list(gcs_url) == {"blobs": [], "prefixes": []}

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_list_dirs_and_blobs(self, get_gc_client, _):
        blob_root_path = "project_path/experiment_id/"
        gcs_url = "gs://bucket/" + blob_root_path

        obj1_mock = mock.Mock()
        file1_path = "fileA"
        obj1_mock.configure_mock(name=blob_root_path + file1_path, size=1)

        obj2_mock = mock.Mock()
        file2_path = "fileB"
        obj2_mock.configure_mock(name=blob_root_path + file2_path, size=0)

        dirname = "model1"
        mock_results = mock.MagicMock()
        mock_results.configure_mock(prefixes=(blob_root_path + dirname + "/",))
        mock_results.__iter__.return_value = [obj1_mock, obj2_mock]

        get_gc_client.return_value.list_blobs.return_value = mock_results

        store = GCSService()
        results = store.list(gcs_url)

        blobs = results["blobs"]
        prefixes = results["prefixes"]
        assert len(blobs) == 2
        assert len(prefixes) == 1
        assert blobs[0][0] == file1_path
        assert blobs[0][1] == obj1_mock.size
        assert blobs[0][1] == 1
        assert blobs[1][0] == file2_path
        assert blobs[1][1] == obj2_mock.size
        assert blobs[1][1] == 0
        assert prefixes[0] == dirname

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_list_with_subdir(self, get_gc_client, _):
        blob_root_path = "project_path/experiment_id/"
        gcs_url = "gs://bucket/" + blob_root_path
        dirname = "model"
        obj_mock = mock.Mock()
        file_path = dirname + "/" + "tf.pb"
        subdirname = dirname + "/" + "files"
        obj_mock.configure_mock(name=blob_root_path + file_path, size=1)

        mock_results = mock.MagicMock()
        mock_results.configure_mock(prefixes=(blob_root_path + subdirname + "/",))
        mock_results.__iter__.return_value = [obj_mock]

        get_gc_client.return_value.list_blobs.return_value = mock_results

        store = GCSService()
        results = store.list(gcs_url, path=dirname)

        blobs = results["blobs"]
        prefixes = results["prefixes"]
        assert len(blobs) == 1
        assert len(prefixes) == 1
        assert blobs[0][0] == file_path
        assert blobs[0][1] == obj_mock.size
        assert prefixes[0] == subdirname

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_upload(self, get_gc_client, _):
        dirname = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"
        open(fpath, "w")

        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.side_effect  # noqa
        ) = os.path.isfile

        store = GCSService()

        # Test without basename
        gcs_url = "gs://bucket/path/to/blob.txt"
        store.upload_file(filename=fpath, blob=gcs_url, use_basename=False)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_called_with(
            "path/to/blob.txt"
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_called_with(  # noqa
                fpath
            )
        )

        # Test with basename
        gcs_url = "gs://bucket/path/to/"
        store.upload_file(filename=fpath, blob=gcs_url, use_basename=True)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_called_with(
            "path/to/test.txt"
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_called_with(  # noqa
                fpath
            )
        )

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_download(self, get_gc_client, _):
        dirname = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"

        def mkfile(fname):
            return open(fname, "w")

        (
            get_gc_client.return_value.get_bucket.return_value.get_blob.return_value.download_to_filename.side_effect  # noqa
        ) = mkfile

        store = GCSService()

        # Test without basename
        gcs_url = "gs://bucket/path/to/blob.txt"
        store.download_file(gcs_url, fpath, use_basename=False)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket().get_blob.assert_called_with(
            "path/to/blob.txt"
        )
        get_gc_client.return_value.get_bucket().get_blob().download_to_filename.assert_called_with(
            fpath
        )

        # Test with basename
        gcs_url = "gs://bucket/path/to/blob.txt"
        store.download_file(gcs_url, dirname, use_basename=True)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket().get_blob.assert_called_with(
            "path/to/blob.txt"
        )
        get_gc_client.return_value.get_bucket().get_blob().download_to_filename.assert_called_with(
            dirname + "/blob.txt"
        )

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_upload_dir(self, get_gc_client, _):
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

        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.side_effect  # noqa
        ) = os.path.isfile

        store = GCSService()

        blob_path = "path/to/"
        gcs_url = "gs://bucket/" + blob_path
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        store.upload_dir(dirname=dirname1, blob=gcs_url, use_basename=False)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_has_calls(
            [
                mock.call("{}test1.txt".format(blob_path)),
                mock.call("{}test2.txt".format(blob_path)),
                mock.call("{}{}/test3.txt".format(blob_path, rel_path2)),
            ],
            any_order=True,
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_has_calls(  # noqa
                [mock.call(fpath1), mock.call(fpath2), mock.call(fpath3)],
                any_order=True,
            )
        )

        # Test with basename
        store.upload_dir(dirname=dirname1, blob=gcs_url, use_basename=True)
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_has_calls(
            [
                mock.call("{}{}/test1.txt".format(blob_path, rel_path1)),
                mock.call("{}{}/test2.txt".format(blob_path, rel_path1)),
                mock.call("{}{}/{}/test3.txt".format(blob_path, rel_path1, rel_path2)),
            ],
            any_order=True,
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_has_calls(  # noqa
                [mock.call(fpath1), mock.call(fpath2), mock.call(fpath3)],
                any_order=True,
            )
        )

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_upload_dir_with_last_time(self, get_gc_client, _):
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

        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.side_effect  # noqa
        ) = os.path.isfile

        store = GCSService()

        blob_path = "path/to/"
        gcs_url = "gs://bucket/" + blob_path
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        store.upload_dir(
            dirname=dirname1, blob=gcs_url, use_basename=False, last_time=last_time
        )
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_has_calls(
            [mock.call("{}{}/test3.txt".format(blob_path, rel_path2))], any_order=True
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_has_calls(  # noqa
                [mock.call(fpath3)], any_order=True
            )
        )

        # Test with basename
        store.upload_dir(
            dirname=dirname1, blob=gcs_url, use_basename=True, last_time=last_time
        )
        get_gc_client.return_value.get_bucket.assert_called_with("bucket")
        get_gc_client.return_value.get_bucket.return_value.blob.assert_has_calls(
            [mock.call("{}{}/{}/test3.txt".format(blob_path, rel_path1, rel_path2))],
            any_order=True,
        )
        (
            get_gc_client.return_value.get_bucket.return_value.blob.return_value.upload_from_filename.assert_has_calls(  # noqa
                [mock.call(fpath3)], any_order=True
            )
        )

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_download_dir(self, get_gc_client, _):
        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        def mkfile(fname):
            return open(fname, "w")

        (
            get_gc_client.return_value.get_bucket.return_value.get_blob.return_value.download_to_filename.side_effect  # noqa
        ) = mkfile

        store = GCSService()

        blob_path = "path/to/"
        gcs_url = "gs://bucket/" + blob_path
        rel_path2 = dirname2.split("/")[-1]

        # Mock return list
        obj_mock1 = mock.Mock()
        obj_mock1.configure_mock(name=blob_path + "test1.txt", size=1)

        obj_mock2 = mock.Mock()
        obj_mock2.configure_mock(name=blob_path + "test2.txt", size=1)

        subdirname = rel_path2 + "/"

        obj_mock3 = mock.Mock()
        obj_mock3.configure_mock(name=blob_path + subdirname + "test3.txt", size=1)

        mock_results = mock.MagicMock()
        mock_results.configure_mock()
        mock_results.__iter__.return_value = [obj_mock1, obj_mock2, obj_mock3]

        get_gc_client.return_value.list_blobs.return_value = mock_results

        dirname3 = tempfile.mkdtemp()

        # Test without basename
        store.download_dir(blob=gcs_url, local_path=dirname3, use_basename=False)
        get_gc_client.return_value.list_blobs.assert_called_with(
            "bucket", prefix=blob_path
        )

        obj_mock1.download_to_filename.assert_called_with(f"{dirname3}/test1.txt")
        obj_mock2.download_to_filename.assert_called_with(f"{dirname3}/test2.txt")
        obj_mock3.download_to_filename.assert_called_with(
            f"{dirname3}/{rel_path2}/test3.txt"
        )

    @mock.patch(GCP_BASE_MODULE.format("get_gc_credentials"))
    @mock.patch(GCP_MODULE.format("get_gc_client"))
    def test_download_dir_with_basename(self, get_gc_client, _):
        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        def mkfile(fname):
            return open(fname, "w")

        (
            get_gc_client.return_value.get_bucket.return_value.get_blob.return_value.download_to_filename.side_effect  # noqa
        ) = mkfile

        store = GCSService()

        blob_path = "path/to/"
        gcs_url = "gs://bucket/" + blob_path
        rel_path2 = dirname2.split("/")[-1]

        # Mock return list
        obj_mock1 = mock.Mock()
        obj_mock1.configure_mock(name=blob_path + "foo/test1.txt", size=1)

        obj_mock2 = mock.Mock()
        obj_mock2.configure_mock(name=blob_path + "foo/test2.txt", size=1)

        subdirname = rel_path2 + "/"

        obj_mock3 = mock.Mock()
        obj_mock3.configure_mock(
            name=blob_path + "foo/" + subdirname + "test3.txt", size=1
        )

        mock_results = mock.MagicMock()
        mock_results.configure_mock()
        mock_results.__iter__.return_value = [obj_mock1, obj_mock2, obj_mock3]

        get_gc_client.return_value.list_blobs.return_value = mock_results

        dirname3 = tempfile.mkdtemp()

        # Test with basename
        store.download_dir(blob=gcs_url + "foo", local_path=dirname3, use_basename=True)
        get_gc_client.return_value.list_blobs.assert_called_with(
            "bucket", prefix=blob_path + "foo"
        )

        obj_mock1.download_to_filename.assert_called_with(f"{dirname3}/foo/test1.txt")
        obj_mock2.download_to_filename.assert_called_with(f"{dirname3}/foo/test2.txt")
        obj_mock3.download_to_filename.assert_called_with(
            f"{dirname3}/foo/{rel_path2}/test3.txt"
        )
