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
import tempfile
import time

from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from moto import mock_s3

from polyaxon.connections.aws.s3 import S3Service
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.utils.date_utils import to_datetime
from tests.utils import BaseTestCase


class TestAwsStore(BaseTestCase):
    def setUp(self):
        super().setUp()
        os.environ["AWS_ACCESS_KEY_ID "] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"
        os.environ["AWS_REGION"] = "us-east-1"

    @mock_s3
    def test_store_client(self):
        store = S3Service(connection="foo", resource="bar")
        assert store.connection == "foo"
        assert store.resource == "bar"

        store = S3Service()
        assert isinstance(store.connection, BaseClient)
        assert isinstance(store.resource, ServiceResource)

    def test_parse_s3_url(self):
        s3_url = "s3://test/this/is/valid/key.txt"
        parsed_url = S3Service.parse_s3_url(s3_url)
        assert parsed_url == ("test", "this/is/valid/key.txt")

    def test_check_prefix_format(self):
        assert S3Service.check_prefix_format(prefix="foo", delimiter="") == "foo"
        assert S3Service.check_prefix_format(prefix="foo", delimiter="/") == "foo/"
        assert S3Service.check_prefix_format(prefix="foo/", delimiter="/") == "foo/"
        assert S3Service.check_prefix_format(prefix="/foo/", delimiter="/") == "/foo/"
        assert (
            S3Service.check_prefix_format(prefix="/foo/boo", delimiter="/")
            == "/foo/boo/"
        )
        assert S3Service.check_prefix_format(prefix="", delimiter="/") == ""

    @mock_s3
    def test_check_bucket(self):
        store = S3Service()
        bucket = store.get_bucket("bucket")
        bucket.create()

        self.assertTrue(store.check_bucket("bucket"))
        self.assertFalse(store.check_bucket("not-a-bucket"))

    def test_check_bucket_raises_with_invalid_client_resources(self):
        store = S3Service(connection="foo", resource="bar")

        with self.assertRaises(Exception):
            store.check_bucket("bucket")

    @mock_s3
    def test_get_bucket(self):
        store = S3Service()
        bucket = store.get_bucket("bucket")
        assert bucket is not None

    @mock_s3
    def test_list_size(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        num_objects = 1001
        for k in range(num_objects):
            b.put_object(Key="a" + str(k), Body=b"a")

        assert (
            len(store.list(bucket_name="bucket", delimiter="/")["keys"]) == num_objects
        )

    @mock_s3
    def test_list_prefixes(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")
        b.put_object(Key="dir/b", Body=b"b")

        assert store.list_prefixes(bucket_name="bucket", prefix="non-existent/") == []
        assert store.list_prefixes(bucket_name="bucket", delimiter="/") == ["dir"]
        assert store.list_keys(bucket_name="bucket", delimiter="/") == [("a", 1)]
        assert store.list_keys(bucket_name="bucket", prefix="dir/") == [("b", 1)]

    @mock_s3
    def test_ls(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")
        b.put_object(Key="dir/b", Body=b"b")

        full_response = {"files": [("a", 1)], "dirs": ["dir"]}
        empty_response = {"dirs": [], "files": []}
        dir_response = {"dirs": [], "files": [("b", 1)]}

        assert store.ls("s3://bucket") == full_response
        assert store.ls("s3://bucket/") == full_response
        assert store.ls("s3://bucket/non-existent") == empty_response
        assert store.ls("s3://bucket/non-existent/") == empty_response
        assert store.ls("s3://bucket/dir") == dir_response
        assert store.ls("s3://bucket/dir/") == dir_response

    @mock_s3
    def test_delete(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")
        b.put_object(Key="dir/b", Body=b"b")

        store.delete(key="a", bucket_name="bucket")
        assert store.list_prefixes(bucket_name="bucket", prefix="non-existent/") == []
        assert store.list_prefixes(bucket_name="bucket", delimiter="/") == ["dir"]
        assert store.list_keys(bucket_name="bucket", delimiter="/") == []
        assert store.list_keys(bucket_name="bucket", prefix="dir/") == [("b", 1)]

    @mock_s3
    def test_list_prefixes_paged(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        # Test only one page
        keys = ["x/b", "y/b"]
        dirs = ["x", "y"]
        for key in keys:
            b.put_object(Key=key, Body=b"a")

        self.assertListEqual(
            sorted(dirs),
            sorted(
                store.list_prefixes(bucket_name="bucket", delimiter="/", page_size=1)
            ),
        )

    @mock_s3
    def test_list_keys(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")
        b.put_object(Key="dir/b", Body=b"b")

        assert store.list_keys(bucket_name="bucket", prefix="non-existent/") == []
        assert store.list_keys(bucket_name="bucket") == [("a", 1), ("dir/b", 1)]
        assert store.list_keys(bucket_name="bucket", delimiter="/") == [("a", 1)]
        assert store.list_keys(bucket_name="bucket", prefix="dir/") == [("b", 1)]

    @mock_s3
    def test_list_keys_paged(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()

        keys = ["x", "y"]
        for key in keys:
            b.put_object(Key=key, Body=b"a")

        self.assertListEqual(
            sorted([(k, 1) for k in keys]),
            sorted(store.list_keys(bucket_name="bucket", delimiter="/", page_size=2)),
        )

    @mock_s3
    def test_check_key(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")

        assert store.check_key("a", "bucket") is True
        assert store.check_key("s3://bucket//a") is True
        assert store.check_key("b", "bucket") is False
        assert store.check_key("s3://bucket//b") is False

    @mock_s3
    def test_get_key(self):
        store = S3Service()
        b = store.get_bucket("bucket")
        b.create()
        b.put_object(Key="a", Body=b"a")

        assert store.get_key("a", "bucket").key == "a"
        assert store.get_key("s3://bucket/a").key == "a"

        # No bucket
        with self.assertRaises(PolyaxonStoresException):
            store.get_key("a", "nobucket")

    @mock_s3
    def test_read_key(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")
        store.connection.put_object(Bucket="bucket", Key="my_key", Body=b"M\xC3\xA9nar")

        self.assertEqual(store.read_key("my_key", "bucket"), u"Ménar")

    @mock_s3
    def test_upload_string(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")

        store.upload_string(u"Ménar", "my_key", "bucket")
        body = store.resource.Object("bucket", "my_key").get()["Body"].read()

        self.assertEqual(body, b"M\xC3\xA9nar")

    @mock_s3
    def test_upload_bytes(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")

        store.upload_bytes(b"Content", "my_key", "bucket")
        body = store.resource.Object("bucket", "my_key").get()["Body"].read()

        self.assertEqual(body, b"Content")

    @mock_s3
    def test_upload_download(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")

        dirname = tempfile.mkdtemp()
        fpath1 = dirname + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        fpath3 = dirname + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        # Upload
        store.upload_file(fpath1, "my_key1.txt", "bucket", use_basename=False)
        assert store.check_key("my_key1.txt", "bucket") is True

        store.upload_file(fpath2, "my_key2.txt", "bucket", use_basename=False)
        assert store.check_key("my_key2.txt", "bucket") is True

        store.upload_file(fpath3, "foo/", "bucket", use_basename=True)
        assert store.check_key("foo/test3.txt", "bucket") is True

        # Download
        store.download_file(
            "my_key1.txt",
            local_path=dirname + "/foo1.txt",
            bucket_name="bucket",
            use_basename=False,
        )
        assert os.path.basename(dirname + "/foo1.txt") == "foo1.txt"
        assert open(os.path.join(dirname + "/foo1.txt")).read() == "data1"

        dirname2 = tempfile.mkdtemp()
        store.download_file(
            "foo/test3.txt",
            local_path=dirname2,
            bucket_name="bucket",
            use_basename=True,
        )
        assert os.path.basename(dirname2 + "/test3.txt") == "test3.txt"
        assert open(os.path.join(dirname2 + "/test3.txt")).read() == "data3"

    @mock_s3
    def test_upload_download_directory(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")

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

        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without using basename
        # Upload
        store.upload_dir(dirname1, "mykey", "bucket", use_basename=False)
        assert store.check_key("mykey/test1.txt", "bucket") is True
        assert store.check_key("mykey/test2.txt", "bucket") is True
        assert store.check_key("mykey/{}/test3.txt".format(rel_path2), "bucket") is True
        # Download
        dirname3 = tempfile.mkdtemp()
        store.download_dir("mykey", dirname3, "bucket", use_basename=False)
        assert sorted(os.listdir(dirname3)) == sorted(
            [rel_path2, "test1.txt", "test2.txt"]
        )
        assert os.listdir("{}/{}".format(dirname3, rel_path2)) == ["test3.txt"]

        # Test with using basename
        store.upload_dir(dirname1, "mykey", "bucket", use_basename=True)
        assert store.check_key("mykey/{}/test1.txt".format(rel_path1), "bucket") is True
        assert store.check_key("mykey/{}/test2.txt".format(rel_path1), "bucket") is True
        assert (
            store.check_key(
                "mykey/{}/{}/test3.txt".format(rel_path1, rel_path2), "bucket"
            )
            is True
        )
        # Download
        dirname3 = tempfile.mkdtemp()
        store.download_dir(
            "mykey/{}".format(rel_path1), dirname3, "bucket", use_basename=True
        )
        assert os.listdir(dirname3) == [rel_path1]
        assert sorted(os.listdir("{}/{}".format(dirname3, rel_path1))) == sorted(
            [rel_path2, "test1.txt", "test2.txt"]
        )
        assert os.listdir("{}/{}/{}".format(dirname3, rel_path1, rel_path2)) == [
            "test3.txt"
        ]

    @mock_s3
    def test_upload_directory_with_last_time(self):
        store = S3Service()
        store.connection.create_bucket(Bucket="bucket")

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

        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without using basename
        # Upload
        store.upload_dir(
            dirname1, "mykey", "bucket", use_basename=False, last_time=last_time
        )
        assert store.check_key("mykey/test1.txt", "bucket") is False
        assert store.check_key("mykey/test2.txt", "bucket") is False
        assert store.check_key("mykey/{}/test3.txt".format(rel_path2), "bucket") is True

        # Test with using basename
        store.upload_dir(
            dirname1, "mykey", "bucket", use_basename=True, last_time=last_time
        )
        assert (
            store.check_key("mykey/{}/test1.txt".format(rel_path1), "bucket") is False
        )
        assert (
            store.check_key("mykey/{}/test2.txt".format(rel_path1), "bucket") is False
        )
        assert (
            store.check_key(
                "mykey/{}/{}/test3.txt".format(rel_path1, rel_path2), "bucket"
            )
            is True
        )
