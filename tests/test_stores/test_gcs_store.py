# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import mock
import os
import tempfile

from unittest import TestCase

from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.stores.gcs_store import GCSStore

GCS_MODULE = 'polyaxon_stores.clients.gc_client.{}'


class TestGCSStore(TestCase):
    def test_parse_gcs_url(self):
        # Correct url
        gcs_url = 'gs://bucket/path/to/blob'
        parsed_url = GCSStore.parse_gcs_url(gcs_url)
        assert parsed_url == ('bucket', 'path/to/blob')

        # Wrong url
        gcs_url = 'gs:/bucket/path/to/blob'
        with self.assertRaises(PolyaxonStoresException):
            GCSStore.parse_gcs_url(gcs_url)

        # Trailing slash
        gcs_url = 'gs://bucket/path/to/blob/'
        assert GCSStore.parse_gcs_url(gcs_url) == ('bucket', 'path/to/blob/')

        # Bucket only
        gcs_url = 'gs://bucket/'
        assert GCSStore.parse_gcs_url(gcs_url) == ('bucket', '')

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_store_client(self, client, gc_credentials):
        client.return_value = 'client'
        store = GCSStore(client='foo')
        assert store.client == 'foo'

        store = GCSStore()
        assert store.client == 'client'
        assert gc_credentials.call_count == 1
        assert client.call_count == 1

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_existing_object(self, client, _):
        test_bucket = 'test_bucket'
        test_object = 'test_object'

        client.return_value.objects.return_value.get.return_value.execute.return_value = {
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
            "metadata": {
                "md5-hash": "95e614241516ad1b64b3551e50538d25"
            },
            "crc32c": "xgdNfQ==",
            "etag": "CLf4hODk7tkCEAE="
        }

        response = GCSStore().check_blob(blob=test_object, bucket_name=test_bucket)
        assert response is True

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_non_existing_object(self, client, _):
        test_bucket = 'test_bucket'
        test_object = 'test_object'

        (client.return_value.objects.return_value
         .get.return_value.execute.side_effect) = Exception

        response = GCSStore().check_blob(blob=test_object, bucket_name=test_bucket)
        assert response is False

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_get_bucket(self, client, _):
        test_bucket = 'test_bucket'

        client.return_value.get_bucket.return_value = {}

        response = GCSStore().get_bucket(bucket_name=test_bucket)

        assert response == {}

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_get_blob(self, client, _):
        test_bucket = 'test_bucket'
        test_object = 'test_object'

        bucket = mock.MagicMock()
        client.return_value.get_bucket.return_value = bucket
        bucket.get_blob.return_value = {}

        response = GCSStore().get_blob(blob=test_object, bucket_name=test_bucket)

        assert response == {}

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_list_empty(self, client, _):
        gcs_url = 'gs://bucket/path/to/blob'
        store = GCSStore()
        client.return_value.get_bucket.return_value.list_blobs.return_value = mock.MagicMock()
        assert store.list(gcs_url) == {'blobs': [], 'prefixes': []}

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_list_dirs_and_blobs(self, client, _):
        blob_root_path = '/project_path/experiment_id/'
        gcs_url = 'gs://bucket' + blob_root_path

        obj_mock = mock.Mock()
        file_path = 'fileA'
        obj_mock.configure_mock(name=blob_root_path + file_path, size=1)

        dir_mock = mock.Mock()
        dir_name = 'model1'
        dir_mock.configure_mock(prefixes=(blob_root_path + dir_name + '/',))

        mock_results = mock.MagicMock()
        mock_results.configure_mock(pages=[dir_mock])
        mock_results.__iter__.return_value = [obj_mock]

        client.return_value.get_bucket.return_value.list_blobs.return_value = mock_results

        store = GCSStore()
        results = store.list(gcs_url)

        blobs = results['blobs']
        prefixes = results['prefixes']
        assert len(blobs) == 1
        assert len(prefixes) == 1
        assert blobs[0][0] == file_path
        assert blobs[0][1] == obj_mock.size
        assert prefixes[0] == dir_name

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_list_with_subdir(self, client, _):
        blob_root_path = '/project_path/experiment_id/'
        gcs_url = 'gs://bucket' + blob_root_path
        dir_name = 'model'
        obj_mock = mock.Mock()
        file_path = dir_name + '/' + 'tf.pb'
        obj_mock.configure_mock(name=blob_root_path + file_path, size=1)

        subdir_mock = mock.Mock()
        subdir_name = dir_name + '/' + 'files'
        subdir_mock.configure_mock(prefixes=(blob_root_path + subdir_name + '/',))

        mock_results = mock.MagicMock()
        mock_results.configure_mock(pages=[subdir_mock])
        mock_results.__iter__.return_value = [obj_mock]

        client.return_value.get_bucket.return_value.list_blobs.return_value = mock_results

        store = GCSStore()
        results = store.list(gcs_url, path=dir_name)

        blobs = results['blobs']
        prefixes = results['prefixes']
        assert len(blobs) == 1
        assert len(prefixes) == 1
        assert blobs[0][0] == file_path
        assert blobs[0][1] == obj_mock.size
        assert prefixes[0] == subdir_name

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_upload(self, client, _):
        gcs_url = 'gs://bucket/path/to/blob.txt'

        dir_name = tempfile.mkdtemp()
        fpath = dir_name + '/test.txt'
        open(fpath, 'w')

        # This will call isfile on the code path being used,
        # thus testing that it's being called with an actually file path
        (client.return_value
         .get_bucket.return_value
         .blob.return_value
         .upload_from_filename.side_effect) = os.path.isfile

        store = GCSStore()
        store.upload_file(gcs_url, fpath)

        client.return_value.get_bucket.assert_called_with('bucket')
        client.return_value.get_bucket.return_value.get_blob.assert_called_with('path/to/blob.txt')
        (client.return_value
         .get_bucket.return_value
         .get_blob.return_value
         .upload_from_filename.assert_called_with(fpath))

    @mock.patch(GCS_MODULE.format('get_gc_credentials'))
    @mock.patch(GCS_MODULE.format('Client'))
    def test_download(self, client, _):
        gcs_url = 'gs://bucket/path/to/blob.txt'

        dir_name = tempfile.mkdtemp()
        fpath = dir_name + '/test.txt'

        def mkfile(fname):
            return open(fname, 'w')

        (client.return_value
         .get_bucket.return_value
         .get_blob.return_value
         .download_to_filename.side_effect) = mkfile

        store = GCSStore()
        store.download_file(gcs_url, fpath)
        client.return_value.get_bucket.assert_called_with('bucket')
        client.return_value.get_bucket().get_blob.assert_called_with('path/to/blob.txt')
        client.return_value.get_bucket().get_blob().download_to_filename.assert_called_with(fpath)
