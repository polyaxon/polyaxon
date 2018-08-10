# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from six import BytesIO
from six.moves import urllib

from botocore.exceptions import ClientError

from polyaxon_stores.clients import aws_client
from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.logger import logger
from polyaxon_stores.utils import (
    append_basename,
    check_dirname_exists,
    force_bytes,
    get_files_in_current_directory
)


class S3Store(object):
    """S3 store Service using Boto3"""
    ENCRYPTION = "AES256"

    def __init__(self, client=None, resource=None, **kwargs):
        self._client = client
        self._resource = resource
        self._encoding = kwargs.get('encoding', 'utf-8')
        self._endpoint_url = kwargs.get('endpoint_url')
        self._aws_access_key_id = kwargs.get('aws_access_key_id')
        self._aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self._aws_session_token = kwargs.get('aws_session_token')
        self._region_name = kwargs.get('region_name')

    @property
    def client(self):
        if self._client is None:
            self.set_client(endpoint_url=self._endpoint_url,
                            aws_access_key_id=self._aws_access_key_id,
                            aws_secret_access_key=self._aws_secret_access_key,
                            aws_session_token=self._aws_session_token,
                            region_name=self._region_name)
        return self._client

    @property
    def resource(self):
        if self._resource is None:
            self.set_resource(endpoint_url=self._endpoint_url,
                              aws_access_key_id=self._aws_access_key_id,
                              aws_secret_access_key=self._aws_secret_access_key,
                              aws_session_token=self._aws_session_token,
                              region_name=self._region_name)
        return self._resource

    def set_client(self,
                   endpoint_url=None,
                   aws_access_key_id=None,
                   aws_secret_access_key=None,
                   aws_session_token=None,
                   region_name=None):
        """
        Sets a new s3 boto3 client.

        :param endpoint_url: The complete URL to use for the constructed client.
        :type endpoint_url: str
        :param aws_access_key_id: The access key to use when creating the client.
        :type aws_access_key_id: str
        :param aws_secret_access_key: The secret key to use when creating the client.
        :type aws_secret_access_key: str
        :param aws_session_token: The session token to use when creating the client.
        :type aws_session_token: str
        :param region_name: The name of the region associated with the client.
            A client is associated with a single region.
        :type region_name: str

        :return: Service client instance
        """
        self._client = aws_client.get_aws_client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name)

    def set_resource(self,
                     endpoint_url=None,
                     aws_access_key_id=None,
                     aws_secret_access_key=None,
                     aws_session_token=None,
                     region_name=None):
        """
        Sets a new s3 boto3 resource.

        :param endpoint_url: The complete URL to use for the constructed client.
        :type endpoint_url: str
        :param aws_access_key_id: The access key to use when creating the client.
        :type aws_access_key_id: str
        :param aws_secret_access_key: The secret key to use when creating the client.
        :type aws_secret_access_key: str
        :param aws_session_token: The session token to use when creating the client.
        :type aws_session_token: str
        :param region_name: The name of the region associated with the client.
            A client is associated with a single region.
        :type region_name: str

        :return: Service resource instance
        """
        self._resource = aws_client.get_aws_resource(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name)

    @staticmethod
    def parse_s3_url(s3_url):
        """
        Parses and validates an S3 url.

        :return: tuple(bucket_name, key).
        """
        parsed_url = urllib.parse.urlparse(s3_url)
        if not parsed_url.netloc:
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(s3_url))
        else:
            bucket_name = parsed_url.netloc
            key = parsed_url.path.strip('/')
            return bucket_name, key

    @staticmethod
    def check_prefix_format(prefix, delimiter):
        if not delimiter or not prefix:
            return prefix
        return prefix + delimiter if prefix[-1] != delimiter else prefix

    def check_bucket(self, bucket_name):
        """
        Checks if a buckete exists.

        :param bucket_name: Name of the bucket
        :type bucket_name: str
        """
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            logger.info(e.response["Error"]["Message"])
            return False

    def get_bucket(self, bucket_name):
        """
        Gets a bucket by name.

        :param bucket_name: Name of the bucket
        :type bucket_name: str
        """
        return self.resource.Bucket(bucket_name)

    def list(self,
             bucket_name,
             prefix='',
             delimiter='',
             page_size=None,
             max_items=None,
             keys=True,
             prefixes=True):
        """
        Lists prefixes and contents in a bucket under prefix.

        :param bucket_name: the name of the bucket
        :type bucket_name: str
        :param prefix: a key prefix
        :type prefix: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param page_size: pagination size
        :type page_size: int
        :param max_items: maximum items to return
        :type max_items: int
        :param keys: if it should include keys
        :type keys: bool
        :param prefixes: if it should include prefixes
        :type prefixes: bool
        """
        config = {
            'PageSize': page_size,
            'MaxItems': max_items,
        }

        paginator = self.client.get_paginator('list_objects_v2')
        prefix = self.check_prefix_format(prefix=prefix, delimiter=delimiter)
        response = paginator.paginate(Bucket=bucket_name,
                                      Prefix=prefix,
                                      Delimiter=delimiter,
                                      PaginationConfig=config)

        def get_keys(contents):
            list_keys = []
            for cont in contents:
                list_keys.append((cont['Key'][len(prefix):], cont.get('Size')))

            return list_keys

        def get_prefixes(page_prefixes):
            list_prefixes = []
            for pref in page_prefixes:
                list_prefixes.append(pref['Prefix'][len(prefix): -1])
            return list_prefixes

        results = {
            'keys': [],
            'prefixes': []
        }
        for page in response:
            if prefixes:
                results['prefixes'] = get_prefixes(page.get('CommonPrefixes', []))
            if keys:
                results['keys'] = get_keys(page.get('Contents', []))

        return results

    def list_prefixes(self, bucket_name, prefix='', delimiter='', page_size=None, max_items=None):
        """
        Lists prefixes in a bucket under prefix

        :param bucket_name: the name of the bucket
        :type bucket_name: str
        :param prefix: a key prefix
        :type prefix: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param page_size: pagination size
        :type page_size: int
        :param max_items: maximum items to return
        :type max_items: int
        """
        results = self.list(bucket_name=bucket_name,
                            prefix=prefix,
                            delimiter=delimiter,
                            page_size=page_size,
                            max_items=max_items,
                            keys=False,
                            prefixes=True)
        return results['prefixes']

    def list_keys(self, bucket_name, prefix='', delimiter='', page_size=None, max_items=None):
        """
        Lists keys in a bucket under prefix and not containing delimiter

        :param bucket_name: the name of the bucket
        :type bucket_name: str
        :param prefix: a key prefix
        :type prefix: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param page_size: pagination size
        :type page_size: int
        :param max_items: maximum items to return
        :type max_items: int
        """
        results = self.list(bucket_name=bucket_name,
                            prefix=prefix,
                            delimiter=delimiter,
                            page_size=page_size,
                            max_items=max_items,
                            keys=True,
                            prefixes=False)
        return results['keys']

    def check_key(self, key, bucket_name=None):
        """
        Checks if a key exists in a bucket

        :param key: S3 key that will point to the file
        :type key: str
        :param bucket_name: Name of the bucket in which the file is stored
        :type bucket_name: str
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        try:
            self.client.head_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError as e:
            logger.info(e.response["Error"]["Message"])
            return False

    def get_key(self, key, bucket_name=None):
        """
        Returns a boto3.s3.Object

        :param key: the path to the key.
        :type key: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        try:
            obj = self.resource.Object(bucket_name, key)
            obj.load()
            return obj
        except Exception as e:
            raise PolyaxonStoresException(e)

    def read_key(self, key, bucket_name=None):
        """
        Reads a key from S3

        :param key: S3 key that will point to the file.
        :type key: str
        :param bucket_name: Name of the bucket in which the file is stored.
        :type bucket_name: str
        """

        obj = self.get_key(key, bucket_name)
        return obj.get()['Body'].read().decode('utf-8')

    def upload_bytes(self,
                     bytes_data,
                     key,
                     bucket_name=None,
                     overwrite=False,
                     encrypt=False,
                     acl=None):
        """
        Uploads bytes to S3

        This is provided as a convenience to drop a string in S3. It uses the
        boto infrastructure to ship a file to s3.

        :param bytes_data: bytes to set as content for the key.
        :type bytes_data: bytes
        :param key: S3 key that will point to the file.
        :type key: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param overwrite: A flag to decide whether or not to overwrite the key
            if it already exists.
        :type overwrite: bool
        :param encrypt: If True, the file will be encrypted on the server-side
            by S3 and will be stored in an encrypted form while at rest in S3.
        :type encrypt: bool
        :param acl: ACL to use for uploading, e.g. "public-read".
        :type acl: str
        """
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        if not overwrite and self.check_key(key, bucket_name):
            raise ValueError("The key {key} already exists.".format(key=key))

        extra_args = {}
        if encrypt:
            extra_args['ServerSideEncryption'] = self.ENCRYPTION
        if acl:
            extra_args['ACL'] = acl

        filelike_buffer = BytesIO(bytes_data)

        self.client.upload_fileobj(filelike_buffer, bucket_name, key, ExtraArgs=extra_args)

    def upload_string(self,
                      string_data,
                      key,
                      bucket_name=None,
                      overwrite=False,
                      encrypt=False,
                      acl=None,
                      encoding='utf-8'):
        """
        Uploads a string to S3.

        This is provided as a convenience to drop a string in S3. It uses the
        boto infrastructure to ship a file to s3.

        :param string_data: string to set as content for the key.
        :type string_data: str
        :param key: S3 key that will point to the file.
        :type key: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param overwrite: A flag to decide whether or not to overwrite the key
            if it already exists.
        :type overwrite: bool
        :param encrypt: If True, the file will be encrypted on the server-side
            by S3 and will be stored in an encrypted form while at rest in S3.
        :type encrypt: bool
        :param acl: ACL to use for uploading, e.g. "public-read".
        :type acl: str
        :param encoding: Encoding to use.
        :type encoding: str
        """
        self.upload_bytes(force_bytes(string_data, encoding=encoding),
                          key=key,
                          bucket_name=bucket_name,
                          overwrite=overwrite,
                          encrypt=encrypt,
                          acl=acl)

    def upload_file(self,
                    filename,
                    key,
                    bucket_name=None,
                    overwrite=False,
                    encrypt=False,
                    acl=None,
                    use_basename=True):
        """
        Uploads a local file to S3.

        :param filename: name of the file to upload.
        :type filename: str
        :param key: S3 key that will point to the file.
        :type key: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param overwrite: A flag to decide whether or not to overwrite the key
            if it already exists. If replace is False and the key exists, an
            error will be raised.
        :type overwrite: bool
        :param encrypt: If True, the file will be encrypted on the server-side
            by S3 and will be stored in an encrypted form while at rest in S3.
        :type encrypt: bool
        :param acl: ACL to use for uploading, e.g. "public-read".
        :type acl: str
        :param use_basename: whether or not to use the basename of the filename.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            key = append_basename(key, filename)

        if not overwrite and self.check_key(key, bucket_name):
            raise PolyaxonStoresException("The key {} already exists.".format(key))

        extra_args = {}
        if encrypt:
            extra_args['ServerSideEncryption'] = self.ENCRYPTION
        if acl:
            extra_args['ACL'] = acl

        self.client.upload_file(filename, bucket_name, key, ExtraArgs=extra_args)

    def download_file(self, key, local_path, bucket_name=None, use_basename=True):
        """
        Download a file from S3.

        :param key: S3 key that will point to the file.
        :type key: str
        :param local_path: the path to download to.
        :type local_path: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the key.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            local_path = append_basename(local_path, key)

        check_dirname_exists(local_path)

        self.client.download_file(bucket_name, key, local_path)

    def upload_files(self,
                     dirname,
                     key,
                     bucket_name=None,
                     overwrite=False,
                     encrypt=False,
                     acl=None,
                     use_basename=True):
        """
        Uploads a local directory to S3.

        :param dirname: name of the directory to upload.
        :type dirname: str
        :param key: S3 key that will point to the file.
        :type key: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param overwrite: A flag to decide whether or not to overwrite the key
            if it already exists. If replace is False and the key exists, an
            error will be raised.
        :type overwrite: bool
        :param encrypt: If True, the file will be encrypted on the server-side
            by S3 and will be stored in an encrypted form while at rest in S3.
        :type encrypt: bool
        :param acl: ACL to use for uploading, e.g. "public-read".
        :type acl: str
        :param use_basename: whether or not to use the basename of the directory.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            key = append_basename(key, dirname)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_current_directory(dirname) as files:
            for f in files:
                file_key = os.path.join(key, os.path.relpath(f, dirname))
                self.upload_file(filename=f,
                                 key=file_key,
                                 bucket_name=bucket_name,
                                 overwrite=overwrite,
                                 encrypt=encrypt,
                                 acl=acl,
                                 use_basename=False)

    def download_files(self, key, local_path, bucket_name=None, use_basename=True):
        """
        Download a directory from S3.

        :param key: S3 key that will point to the file.
        :type key: str
        :param local_path: the path to download to.
        :type local_path: str
        :param bucket_name: Name of the bucket in which to store the file.
        :type bucket_name: str
        :param use_basename: whether or not to use the basename of the key.
        :type use_basename: bool
        """
        if not bucket_name:
            bucket_name, key = self.parse_s3_url(key)

        if use_basename:
            local_path = append_basename(local_path, key)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonStoresException:
            os.mkdir(local_path)

        results = self.list(bucket_name=bucket_name, prefix=key, delimiter='/')

        # Create directories
        for prefix in sorted(results['prefixes']):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(key, prefix)
            # Download files under
            self.download_files(key=prefix,
                                local_path=direname,
                                bucket_name=bucket_name,
                                use_basename=False)

        # Download files
        for file_key in results['keys']:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(key, file_key)
            self.download_file(key=file_key,
                               local_path=filename,
                               bucket_name=bucket_name,
                               use_basename=False)
