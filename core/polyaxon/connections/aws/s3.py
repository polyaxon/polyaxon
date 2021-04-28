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

from concurrent import futures
from io import BytesIO
from typing import List

from botocore.exceptions import ClientError

from polyaxon.connections.aws import base
from polyaxon.connections.aws.base import AWSService
from polyaxon.exceptions import (
    PolyaxonPathException,
    PolyaxonSchemaError,
    PolyaxonStoresException,
)
from polyaxon.logger import logger
from polyaxon.parser import parser
from polyaxon.stores.base_store import StoreMixin
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.path_utils import (
    append_basename,
    check_dirname_exists,
    get_files_in_path_context,
)
from polyaxon.utils.string_utils import force_bytes


class S3Service(AWSService, StoreMixin):
    """
    S3 store Service using Boto3.
    """

    RESOURCE_TYPE = "s3"

    @staticmethod
    def parse_s3_url(s3_url):
        """
        Parses and validates an S3 url.

        Returns:
             tuple(bucket_name, key).
        """
        try:
            spec = parser.parse_s3_path(s3_url)
            return spec.bucket, spec.key
        except PolyaxonSchemaError as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

    @staticmethod
    def check_prefix_format(prefix, delimiter):
        if not delimiter or not prefix:
            return prefix
        return prefix + delimiter if prefix[-1] != delimiter else prefix

    def check_bucket(self, bucket_name):
        """
        Checks if a buckete exists.

        Args:
            bucket_name: `str`. Name of the bucket
        """
        try:
            self.connection.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            logger.info(e.response["Error"]["Message"])
            return False

    def get_bucket(self, bucket_name):
        """
        Gets a bucket by name.

        Args:
            bucket_name: `str`. Name of the bucket
        """
        return self.resource.Bucket(bucket_name)

    def ls(self, path):
        (bucket_name, key) = self.parse_s3_url(path)
        results = self.list(bucket_name=bucket_name, prefix=key)
        return {"files": results["keys"], "dirs": results["prefixes"]}

    def list(
        self,
        bucket_name,
        prefix="",
        delimiter="/",
        page_size=None,
        max_items=None,
        keys=True,
        prefixes=True,
    ):
        """
        Lists prefixes and contents in a bucket under prefix.

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `str`. pagination size
            max_items: `int`. maximum items to return
            keys: `bool`. if it should include keys
            prefixes: `boll`. if it should include prefixes
        """
        config = {"PageSize": page_size, "MaxItems": max_items}

        legacy_api = base.get_legacy_api(legacy_api=self._aws_legacy_api)

        if legacy_api:
            paginator = self.connection.get_paginator("list_objects")
        else:
            paginator = self.connection.get_paginator("list_objects_v2")

        prefix = self.check_prefix_format(prefix=prefix, delimiter=delimiter)
        response = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix,
            Delimiter=delimiter,
            PaginationConfig=config,
        )

        def get_keys(contents):
            list_keys = []
            for cont in contents:
                list_keys.append((cont["Key"][len(prefix) :], cont.get("Size")))

            return list_keys

        def get_prefixes(page_prefixes):
            list_prefixes = []
            for pref in page_prefixes:
                list_prefixes.append(pref["Prefix"][len(prefix) : -1])
            return list_prefixes

        results = {"keys": [], "prefixes": []}
        for page in response:
            if prefixes:
                results["prefixes"] += get_prefixes(page.get("CommonPrefixes", []))
            if keys:
                results["keys"] += get_keys(page.get("Contents", []))

        return results

    def list_prefixes(
        self, bucket_name, prefix="", delimiter="", page_size=None, max_items=None
    ):
        """
        Lists prefixes in a bucket under prefix

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `int`. pagination size
            max_items: `int`. maximum items to return
        """
        results = self.list(
            bucket_name=bucket_name,
            prefix=prefix,
            delimiter=delimiter,
            page_size=page_size,
            max_items=max_items,
            keys=False,
            prefixes=True,
        )
        return results["prefixes"]

    def list_keys(
        self, bucket_name, prefix="", delimiter="", page_size=None, max_items=None
    ):
        """
        Lists keys in a bucket under prefix and not containing delimiter

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `int`. pagination size
            max_items: `int`. maximum items to return
        """
        results = self.list(
            bucket_name=bucket_name,
            prefix=prefix,
            delimiter=delimiter,
            page_size=page_size,
            max_items=max_items,
            keys=True,
            prefixes=False,
        )
        return results["keys"]

    def check_key(self, key, bucket_name=None):
        """
        Checks if a key exists in a bucket

        Args:
            key: `str`. S3 key that will point to the file
            bucket_name: `str`. Name of the bucket in which the file is stored
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        try:
            self.connection.head_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError as e:
            logger.info(e.response["Error"]["Message"])
            return False

    def get_key(self, key, bucket_name=None):
        """
        Returns a boto3.s3.Object

        Args:
            key: `str`. the path to the key.
            bucket_name: `str`. the name of the bucket.
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        try:
            obj = self.resource.Object(bucket_name, key)
            obj.load()
            return obj
        except Exception as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

    def read_key(self, key, bucket_name=None):
        """
        Reads a key from S3

        Args:
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which the file is stored.
        """

        obj = self.get_key(key, bucket_name)
        return obj.get()["Body"].read().decode("utf-8")

    def upload_bytes(
        self,
        bytes_data,
        key,
        bucket_name=None,
        overwrite=True,
        encrypt=False,
        acl=None,
    ):
        """
        Uploads bytes to S3

        This is provided as a convenience to drop a string in S3. It uses the
        boto infrastructure to ship a file to s3.

        Args:
            bytes_data: `bytes`. bytes to set as content for the key.
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which to store the file.
            overwrite: `bool`. A flag to decide whether or not to overwrite the key
                if it already exists.
            encrypt: `bool`. If True, the file will be encrypted on the server-side
                by S3 and will be stored in an encrypted form while at rest in S3.
            acl: `str`. ACL to use for uploading, e.g. "public-read".
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        if not overwrite and self.check_key(key, bucket_name):
            raise ValueError("The key {key} already exists.".format(key=key))

        extra_args = {}
        if encrypt:
            extra_args["ServerSideEncryption"] = self.ENCRYPTION
        if acl:
            extra_args["ACL"] = acl

        filelike_buffer = BytesIO(bytes_data)

        self.connection.upload_fileobj(
            filelike_buffer, bucket_name, key, ExtraArgs=extra_args
        )

    def upload_string(
        self,
        string_data,
        key,
        bucket_name=None,
        overwrite=True,
        encrypt=False,
        acl=None,
        encoding="utf-8",
    ):
        """
        Uploads a string to S3.

        This is provided as a convenience to drop a string in S3. It uses the
        boto infrastructure to ship a file to s3.

        Args:
            string_data: `str`. string to set as content for the key.
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which to store the file.
            overwrite: `bool`. A flag to decide whether or not to overwrite the key
                if it already exists.
            encrypt: `bool`. If True, the file will be encrypted on the server-side
                by S3 and will be stored in an encrypted form while at rest in S3.
            acl: `str`. ACL to use for uploading, e.g. "public-read".
            encoding: `str`. Encoding to use.
        """
        self.upload_bytes(
            force_bytes(string_data, encoding=encoding),
            key=key,
            bucket_name=bucket_name,
            overwrite=overwrite,
            encrypt=encrypt,
            acl=acl,
        )

    def upload_file(
        self,
        filename,
        key,
        bucket_name=None,
        overwrite=True,
        encrypt=False,
        acl=None,
        use_basename=True,
    ):
        """
        Uploads a local file to S3.

        Args:
            filename: `str`. name of the file to upload.
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which to store the file.
            overwrite: `bool`. A flag to decide whether or not to overwrite the key
                if it already exists. If replace is False and the key exists, an
                error will be raised.
            encrypt: `bool`. If True, the file will be encrypted on the server-side
                by S3 and will be stored in an encrypted form while at rest in S3.
            acl: `str`. ACL to use for uploading, e.g. "public-read".
            use_basename: `bool`. whether or not to use the basename of the filename.
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            key = append_basename(key, filename)

        if not overwrite and self.check_key(key, bucket_name):
            raise PolyaxonStoresException("The key {} already exists.".format(key))

        extra_args = {}
        if encrypt:
            extra_args["ServerSideEncryption"] = self.ENCRYPTION
        if acl:
            extra_args["ACL"] = acl

        self.connection.upload_file(filename, bucket_name, key, ExtraArgs=extra_args)

    def download_file(self, key, local_path, bucket_name=None, use_basename=True):
        """
        Download a file from S3.

        Args:
            key: `str`. S3 key that will point to the file.
            local_path: `str`. the path to download to.
            bucket_name: `str`. Name of the bucket in which to store the file.
            use_basename: `bool`. whether or not to use the basename of the key.
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, key)

        try:
            check_dirname_exists(local_path)
        except PolyaxonPathException as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

        try:
            self.connection.download_file(bucket_name, key, local_path)
        except ClientError as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

    def upload_dir(
        self,
        dirname,
        key,
        bucket_name=None,
        overwrite=True,
        encrypt=False,
        acl=None,
        use_basename=True,
        workers=0,
        last_time=None,
        exclude: List[str] = None,
    ):
        """
        Uploads a local directory to S3.

        Args:
            dirname: `str`. name of the directory to upload.
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which to store the file.
            overwrite: `bool`. A flag to decide whether or not to overwrite the key
                if it already exists. If replace is False and the key exists, an
                error will be raised.
            encrypt: `bool`. If True, the file will be encrypted on the server-side
                by S3 and will be stored in an encrypted form while at rest in S3.
            acl: `str`. ACL to use for uploading, e.g. "public-read".
            use_basename: `bool`. whether or not to use the basename of the directory.
            last_time: `datetime`. if provided,
                        it will only upload the file if changed after last_time.
            exclude: `list`. List of paths to excludes.
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            key = append_basename(key, dirname)

        pool, future_results = self.init_pool(workers)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_path_context(dirname, exclude=exclude) as files:
            for f in files:

                # If last time is provided we check if we should re-upload the file
                if last_time and not file_modified_since(
                    filepath=f, last_time=last_time
                ):
                    continue

                file_key = os.path.join(key, os.path.relpath(f, dirname))
                future_results = self.submit_pool(
                    workers=workers,
                    pool=pool,
                    future_results=future_results,
                    fn=self.upload_file,
                    filename=f,
                    key=file_key,
                    bucket_name=bucket_name,
                    overwrite=overwrite,
                    encrypt=encrypt,
                    acl=acl,
                    use_basename=False,
                )
        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def download_dir(
        self,
        key: str,
        local_path: str,
        bucket_name: str = None,
        use_basename: bool = True,
        workers: int = 0,
    ):
        """
        Download a directory from S3.

        Args:
            key: `str`. S3 key that will point to the file.
            local_path: `str`. the path to download to.
            bucket_name: `str`. Name of the bucket in which to store the file.
            use_basename: `bool`. whether or not to use the basename of the key.
            workers: number of workers threads to use for parallel execution.
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, key)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonPathException:
            os.makedirs(local_path)

        results = self.list(bucket_name=bucket_name, prefix=key, delimiter="/")

        # Create directories
        for prefix in sorted(results["prefixes"]):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(key, prefix)
            # Download files under
            self.download_dir(
                key=prefix,
                local_path=direname,
                bucket_name=bucket_name,
                use_basename=False,
            )

        pool, future_results = self.init_pool(workers)

        # Download files
        for file_key in results["keys"]:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(key, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.download_file,
                key=file_key,
                local_path=filename,
                bucket_name=bucket_name,
                use_basename=False,
            )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def delete(self, key, bucket_name=None, workers=0):
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        results = self.list(bucket_name=bucket_name, prefix=key, delimiter="/")

        if not any([results["prefixes"], results["keys"]]):
            self.delete_file(key=key, bucket_name=bucket_name)

        # Delete directories
        for prefix in sorted(results["prefixes"]):
            prefix = os.path.join(key, prefix)
            # Deletes files under
            self.delete(key=prefix, bucket_name=bucket_name)

        pool, future_results = self.init_pool(workers)

        # Delete files
        for file_key in results["keys"]:
            file_key = file_key[0]
            file_key = os.path.join(key, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.delete_file,
                key=file_key,
                bucket_name=bucket_name,
            )
        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def delete_file(self, key, bucket_name=None):
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)
        try:
            obj = self.resource.Object(bucket_name, key)
            obj.delete()
        except ClientError as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e
