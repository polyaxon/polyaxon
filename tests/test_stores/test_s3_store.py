# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tempfile

from unittest import TestCase

from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from moto import mock_s3

from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.stores.s3_store import S3Store


class TestAwsStore(TestCase):
    @mock_s3
    def test_store_client(self):
        store = S3Store(client='foo', resource='bar')
        assert store.client == 'foo'
        assert store.resource == 'bar'

        store = S3Store()
        assert isinstance(store.client, BaseClient)
        assert isinstance(store.resource, ServiceResource)

    def test_parse_s3_url(self):
        s3_url = 's3://test/this/is/bad/key.txt'
        parsed_url = S3Store.parse_s3_url(s3_url)
        assert parsed_url == ('test', 'this/is/bad/key.txt')

    @mock_s3
    def test_check_bucket(self):
        store = S3Store()
        bucket = store.get_bucket('bucket')
        bucket.create()

        self.assertTrue(store.check_bucket('bucket'))
        self.assertFalse(store.check_bucket('not-a-bucket'))

    def test_check_bucket_raises_with_invalid_client_resources(self):
        store = S3Store(client='foo', resource='bar')

        with self.assertRaises(Exception):
            store.check_bucket('bucket')

    @mock_s3
    def test_get_bucket(self):
        store = S3Store()
        bucket = store.get_bucket('bucket')
        assert bucket is not None

    @mock_s3
    def test_list_prefixes(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()
        b.put_object(Key='a', Body=b'a')
        b.put_object(Key='dir/b', Body=b'b')

        assert store.list_prefixes(bucket_name='bucket', prefix='non-existent/') == []
        assert store.list_prefixes(bucket_name='bucket', delimiter='/') == ['dir/']
        assert store.list_keys(bucket_name='bucket', delimiter='/') == [('a', 1)]
        assert store.list_keys(bucket_name='bucket', prefix='dir/') == [('dir/b', 1)]

    @mock_s3
    def test_list_prefixes_paged(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()
        # Test only one page
        keys = ['x/b', 'y/b']
        dirs = ['x/', 'y/']
        for key in keys:
            b.put_object(Key=key, Body=b'a')

        self.assertListEqual(sorted(dirs),
                             sorted(store.list_prefixes(bucket_name='bucket',
                                                        delimiter='/',
                                                        page_size=1)))

    @mock_s3
    def test_list_keys(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()
        b.put_object(Key='a', Body=b'a')
        b.put_object(Key='dir/b', Body=b'b')

        assert store.list_keys(bucket_name='bucket', prefix='non-existent/') == []
        assert store.list_keys(bucket_name='bucket') == [('a', 1), ('dir/b', 1)]
        assert store.list_keys(bucket_name='bucket', delimiter='/') == [('a', 1)]
        assert store.list_keys(bucket_name='bucket', prefix='dir/') == [('dir/b', 1)]

    @mock_s3
    def test_list_keys_paged(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()

        keys = ['x', 'y']
        for key in keys:
            b.put_object(Key=key, Body=b'a')

        self.assertListEqual(sorted([(k, 1) for k in keys]),
                             sorted(store.list_keys(bucket_name='bucket',
                                                    delimiter='/',
                                                    page_size=2)))

    @mock_s3
    def test_check_key(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()
        b.put_object(Key='a', Body=b'a')

        assert store.check_key('a', 'bucket') is True
        assert store.check_key('s3://bucket//a') is True
        assert store.check_key('b', 'bucket') is False
        assert store.check_key('s3://bucket//b') is False

    @mock_s3
    def test_get_key(self):
        store = S3Store()
        b = store.get_bucket('bucket')
        b.create()
        b.put_object(Key='a', Body=b'a')

        assert store.get_key('a', 'bucket').key == 'a'
        assert store.get_key('s3://bucket/a').key == 'a'

        # No bucket
        with self.assertRaises(PolyaxonStoresException):
            store.get_key('a', 'nobucket')

    @mock_s3
    def test_read_key(self):
        store = S3Store()
        store.client.create_bucket(Bucket='bucket')
        store.client.put_object(Bucket='bucket', Key='my_key', Body=b'M\xC3\xA9nar')

        self.assertEqual(store.read_key('my_key', 'bucket'), u'Ménar')

    @mock_s3
    def test_upload_string(self):
        store = S3Store()
        store.client.create_bucket(Bucket='bucket')

        store.upload_string(u'Ménar', 'my_key', 'bucket')
        body = store.resource.Object('bucket', 'my_key').get()['Body'].read()

        self.assertEqual(body, b'M\xC3\xA9nar')

    @mock_s3
    def test_upload_bytes(self):
        store = S3Store()
        store.client.create_bucket(Bucket='bucket')

        store.upload_bytes(b'Content', 'my_key', 'bucket')
        body = store.resource.Object('bucket', 'my_key').get()['Body'].read()

        self.assertEqual(body, b'Content')

    @mock_s3
    def test_upload_download(self):
        store = S3Store()
        store.client.create_bucket(Bucket='bucket')

        dir_name = tempfile.mkdtemp()
        fpath1 = dir_name + '/test1.txt'
        with open(fpath1, 'w') as f:
            f.write('data1')

        fpath2 = dir_name + '/test2.txt'
        with open(fpath2, 'w') as f:
            f.write('data2')

        fpath3 = dir_name + '/test3.txt'
        with open(fpath3, 'w') as f:
            f.write('data3')

        store.upload_file(fpath1, 'my_key1.txt', 'bucket', use_basename=False)
        assert store.check_key('my_key1.txt', 'bucket') is True

        store.upload_file(fpath2, 'my_key2.txt', 'bucket', use_basename=False)
        assert store.check_key('my_key2.txt', 'bucket') is True

        store.upload_file(fpath3, 'foo/', 'bucket', use_basename=True)
        assert store.check_key('foo/test3.txt', 'bucket') is True

        store.download_file('my_key1.txt',
                            local_path=dir_name + '/foo1.txt',
                            bucket_name='bucket',
                            use_basename=False)
        assert os.path.basename(dir_name + '/foo1.txt') == 'foo1.txt'
        assert open(os.path.join(dir_name + '/foo1.txt')).read() == 'data1'

        dir_name2 = tempfile.mkdtemp()
        store.download_file('foo/test3.txt',
                            local_path=dir_name2,
                            bucket_name='bucket',
                            use_basename=True)
        assert os.path.basename(dir_name2 + '/test3.txt') == 'test3.txt'
        assert open(os.path.join(dir_name2 + '/test3.txt')).read() == 'data3'

    @mock_s3
    def test_upload_files(self):
        store = S3Store()
        store.client.create_bucket(Bucket='bucket')

        dir_name1 = tempfile.mkdtemp()
        fpath1 = dir_name1 + '/test1.txt'
        with open(fpath1, 'w') as f:
            f.write('data1')

        fpath2 = dir_name1 + '/test2.txt'
        with open(fpath2, 'w') as f:
            f.write('data2')

        dir_name2 = tempfile.mkdtemp(prefix=dir_name1 + '/')
        fpath3 = dir_name2 + '/test3.txt'
        with open(fpath3, 'w') as f:
            f.write('data3')

        rel_path1 = dir_name1.split('/')[-1]
        rel_path2 = dir_name2.split('/')[-1]

        # Test without using basename
        store.upload_files(dir_name1, 'mykey', 'bucket', use_basename=False)
        assert store.check_key('mykey/test1.txt', 'bucket') is True
        assert store.check_key('mykey/test2.txt', 'bucket') is True
        assert store.check_key('mykey/{}/test3.txt'.format(rel_path2), 'bucket') is True

        # Test with using basename
        store.upload_files(dir_name1, 'mykey', 'bucket', use_basename=True)
        assert store.check_key('mykey/{}/test1.txt'.format(rel_path1), 'bucket') is True
        assert store.check_key('mykey/{}/test2.txt'.format(rel_path1), 'bucket') is True
        assert store.check_key(
            'mykey/{}/{}/test3.txt'.format(rel_path1, rel_path2), 'bucket') is True
