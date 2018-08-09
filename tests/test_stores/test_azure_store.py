# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import mock
import tempfile

from unittest import TestCase

from azure.storage.blob import Blob, BlobPrefix, BlobProperties

from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.stores.azure_store import AzureStore

AZURE_MODULE = 'polyaxon_stores.clients.azure_client.{}'


class MockBlobList(object):
    def __init__(self, items, next_marker=None):
        self.items = items
        self.next_marker = next_marker

    def __iter__(self):
        return iter(self.items)


class TestAzureStore(TestCase):
    def setUp(self):
        self.wasbs_base = 'wasbs://container@user.blob.core.windows.net/'

    def test_parse_wasbs_url(self):
        # Correct url
        wasbs_url = 'wasbs://container@user.blob.core.windows.net/path'
        parsed_url = AzureStore.parse_wasbs_url(wasbs_url)
        assert parsed_url == ('container', 'user', 'path')
        wasbs_url = 'wasbs://container@user.blob.core.windows.net/'
        parsed_url = AzureStore.parse_wasbs_url(wasbs_url)
        assert parsed_url == ('container', 'user', '')
        wasbs_url = 'wasbs://container@user.blob.core.windows.net'
        parsed_url = AzureStore.parse_wasbs_url(wasbs_url)
        assert parsed_url == ('container', 'user', '')
        wasbs_url = 'wasbs://container@user.blob.core.windows.net/path/to/file'
        parsed_url = AzureStore.parse_wasbs_url(wasbs_url)
        assert parsed_url == ('container', 'user', 'path/to/file')

        # Wrong url
        wasbs_url = 'wasbs://container@user.foo.bar.windows.net/path/to/file'
        with self.assertRaises(PolyaxonStoresException):
            AzureStore.parse_wasbs_url(wasbs_url)

        wasbs_url = 'wasbs://container@user.blob.core.foo.net/path/to/file'
        with self.assertRaises(PolyaxonStoresException):
            AzureStore.parse_wasbs_url(wasbs_url)

        wasbs_url = 'wasbs://container@user.blob.windows.net/path/to/file'
        with self.assertRaises(PolyaxonStoresException):
            AzureStore.parse_wasbs_url(wasbs_url)

    @mock.patch(AZURE_MODULE.format('BlockBlobService'))
    def test_list_empty(self, client):
        client.return_value.list_blobs.return_value = MockBlobList([])

        store = AzureStore()
        key_path = self.wasbs_base + 'path'
        assert store.list(key=key_path) == {'blobs': [], 'prefixes': []}

    @mock.patch(AZURE_MODULE.format('BlockBlobService'))
    def test_list_non_empty(self, client):
        base_path = 'path'
        # Create some files to return
        dir_prefix = BlobPrefix()
        dir_prefix.name = base_path + '/dir'

        blob_props = BlobProperties()
        blob_props.content_length = 42
        blob = Blob(base_path + '/file', props=blob_props)

        client.return_value.list_blobs.return_value = MockBlobList([dir_prefix, blob])

        store = AzureStore()
        key_path = self.wasbs_base + base_path
        results = store.list(key=key_path)
        assert len(results['blobs']) == 1
        assert len(results['prefixes']) == 1
        assert results['prefixes'][0] == 'dir'
        assert results['blobs'][0][0] == 'file'
        assert results['blobs'][0][1] == 42

    @mock.patch(AZURE_MODULE.format('BlockBlobService'))
    def test_upload_file(self, client):
        dir_name = tempfile.mkdtemp()
        fpath = dir_name + '/test.txt'
        open(fpath, 'w')

        base_path = 'path/'
        base_path_file = base_path + 'test.txt'
        store = AzureStore()

        # Test without basename
        key_path = self.wasbs_base + base_path_file
        store.upload_file(key_path, fpath, use_basename=False)
        client.return_value.create_blob_from_path.assert_called_with(
            'container', base_path_file, fpath)

        # Test with basename
        key_path = self.wasbs_base + base_path
        store.upload_file(key_path, fpath, use_basename=True)
        client.return_value.create_blob_from_path.assert_called_with(
            'container', base_path_file, fpath)

    @mock.patch(AZURE_MODULE.format('BlockBlobService'))
    def test_download_file(self, client):
        client.return_value.list_blobs.return_value = MockBlobList([])

        dir_name = tempfile.mkdtemp()
        fpath = dir_name + '/test.txt'

        def mkfile(container, cloud_path, fname):
            return open(fname, 'w')

        client.return_value.get_blob_to_path.side_effect = mkfile

        base_path = 'path/test.txt'
        store = AzureStore()
        key_path = self.wasbs_base + base_path

        # Test without basename
        store.download_file(key_path, fpath, use_basename=False)
        client.return_value.get_blob_to_path.assert_called_with(
            "container", base_path, fpath)

        # Test without basename
        store.download_file(key_path, dir_name, use_basename=True)
        client.return_value.get_blob_to_path.assert_called_with(
            "container", base_path, fpath)
