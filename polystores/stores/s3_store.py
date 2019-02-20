# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from six import BytesIO
from six.moves import urllib

from botocore.exceptions import ClientError

from polystores.clients import aws_client
from polystores.exceptions import PolyaxonStoresException
from polystores.logger import logger
from polystores.stores.base_store import BaseStore
from polystores.utils import (
    append_basename,
    check_dirname_exists,
    force_bytes,
    get_files_in_current_directory
)

# pylint:disable=arguments-differ


class S3Store(BaseStore):
    """
    S3 store Service using Boto3.
    """
    STORE_TYPE = BaseStore._S3_STORE  # pylint:disable=protected-access
    ENCRYPTION = "AES256"

    def __init__(self, client=None, resource=None, **kwargs):
        self._client = client
        self._resource = resource
        self._encoding = kwargs.get('encoding', 'utf-8')
        self._endpoint_url = (kwargs.get('endpoint_url') or
                              kwargs.get('aws_endpoint_url') or
                              kwargs.get('AWS_ENDPOINT_URL'))
        self._aws_access_key_id = (kwargs.get('access_key_id') or
                                   kwargs.get('aws_access_key_id') or
                                   kwargs.get('AWS_ACCESS_KEY_ID'))
        self._aws_secret_access_key = (kwargs.get('secret_access_key') or
                                       kwargs.get('aws_secret_access_key') or
                                       kwargs.get('AWS_SECRET_ACCESS_KEY'))
        self._aws_session_token = (kwargs.get('session_token') or
                                   kwargs.get('aws_session_token') or
                                   kwargs.get('AWS_SECURITY_TOKEN'))
        self._region_name = (kwargs.get('region') or
                             kwargs.get('aws_region') or
                             kwargs.get('AWS_REGION'))
        self._aws_verify_ssl = kwargs.get('verify_ssl',
                                          kwargs.get('aws_verify_ssl',
                                                     kwargs.get('AWS_VERIFY_SSL', None)))
        self._aws_use_ssl = (kwargs.get('use_ssl') or
                             kwargs.get('aws_use_ssl') or
                             kwargs.get('AWS_USE_SSL'))
        self._aws_legacy_api = (kwargs.get('legacy_api') or
                                kwargs.get('aws_legacy_api') or
                                kwargs.get('AWS_LEGACY_API'))

    @property
    def client(self):
        if self._client is None:
            self.set_client(endpoint_url=self._endpoint_url,
                            aws_access_key_id=self._aws_access_key_id,
                            aws_secret_access_key=self._aws_secret_access_key,
                            aws_session_token=self._aws_session_token,
                            region_name=self._region_name,
                            aws_use_ssl=self._aws_use_ssl,
                            aws_verify_ssl=self._aws_verify_ssl)
        return self._client

    def set_env_vars(self):
        if self._endpoint_url:
            os.environ['AWS_ENDPOINT_URL'] = self._endpoint_url
        if self._aws_access_key_id:
            os.environ['AWS_ACCESS_KEY_ID'] = self._aws_access_key_id
        if self._aws_secret_access_key:
            os.environ['AWS_SECRET_ACCESS_KEY'] = self._aws_secret_access_key
        if self._aws_session_token:
            os.environ['AWS_SECURITY_TOKEN'] = self._aws_session_token
        if self._region_name:
            os.environ['AWS_REGION'] = self._region_name
        if self._aws_use_ssl is not None:
            os.environ['AWS_USE_SSL'] = self._aws_use_ssl
        if self._aws_verify_ssl is not None:
            os.environ['AWS_VERIFY_SSL'] = self._aws_verify_ssl
        if self._aws_legacy_api:
            os.environ['AWS_LEGACY_API'] = self._aws_legacy_api

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
                   region_name=None,
                   aws_use_ssl=True,
                   aws_verify_ssl=None):
        """
        Sets a new s3 boto3 client.

        Args:
            endpoint_url: `str`. The complete URL to use for the constructed client.
            aws_access_key_id: `str`. The access key to use when creating the client.
            aws_secret_access_key: `str`. The secret key to use when creating the client.
            aws_session_token: `str`. The session token to use when creating the client.
            region_name: `str`. The name of the region associated with the client.
                A client is associated with a single region.

        Returns:
            Service client instance
        """
        self._client = aws_client.get_aws_client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            aws_use_ssl=aws_use_ssl,
            aws_verify_ssl=aws_verify_ssl)

    def set_resource(self,
                     endpoint_url=None,
                     aws_access_key_id=None,
                     aws_secret_access_key=None,
                     aws_session_token=None,
                     region_name=None):
        """
        Sets a new s3 boto3 resource.

        Args:
            endpoint_url: `str`. The complete URL to use for the constructed client.
            aws_access_key_id: `str`. The access key to use when creating the client.
            aws_secret_access_key: `str`. The secret key to use when creating the client.
            aws_session_token: `str`. The session token to use when creating the client.
            region_name: `str`. The name of the region associated with the client.
                A client is associated with a single region.

        Returns:
             Service resource instance
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

        Returns:
             tuple(bucket_name, key).
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

        Args:
            bucket_name: `str`. Name of the bucket
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

        Args:
            bucket_name: `str`. Name of the bucket
        """
        return self.resource.Bucket(bucket_name)

    def ls(self, path):
        results = self.list(bucket_name=path)
        return {'files': results['keys'], 'dirs': results['prefixes']}

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

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `str`. pagination size
            max_items: `int`. maximum items to return
            keys: `bool`. if it should include keys
            prefixes: `boll`. if it should include prefixes
        """
        config = {
            'PageSize': page_size,
            'MaxItems': max_items,
        }

        legacy_api = aws_client.get_legacy_api(legacy_api=self._aws_legacy_api)

        if legacy_api:
            paginator = self.client.get_paginator('list_objects')
        else:
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
                results['prefixes'] += get_prefixes(page.get('CommonPrefixes', []))
            if keys:
                results['keys'] += get_keys(page.get('Contents', []))

        return results

    def list_prefixes(self, bucket_name, prefix='', delimiter='', page_size=None, max_items=None):
        """
        Lists prefixes in a bucket under prefix

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `int`. pagination size
            max_items: `int`. maximum items to return
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

        Args:
            bucket_name: `str`. the name of the bucket
            prefix: `str`. a key prefix
            delimiter: `str`. the delimiter marks key hierarchy.
            page_size: `int`. pagination size
            max_items: `int`. maximum items to return
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

        Args:
            key: `str`. S3 key that will point to the file
            bucket_name: `str`. Name of the bucket in which the file is stored
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
            raise PolyaxonStoresException(e)

    def read_key(self, key, bucket_name=None):
        """
        Reads a key from S3

        Args:
            key: `str`. S3 key that will point to the file.
            bucket_name: `str`. Name of the bucket in which the file is stored.
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
            extra_args['ServerSideEncryption'] = self.ENCRYPTION
        if acl:
            extra_args['ACL'] = acl

        self.client.upload_file(filename, bucket_name, key, ExtraArgs=extra_args)

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

        check_dirname_exists(local_path)

        try:
            self.client.download_file(bucket_name, key, local_path)
        except ClientError as e:
            raise PolyaxonStoresException(e)

    def upload_dir(self,
                   dirname,
                   key,
                   bucket_name=None,
                   overwrite=False,
                   encrypt=False,
                   acl=None,
                   use_basename=True):
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

    def download_dir(self, key, local_path, bucket_name=None, use_basename=True):
        """
        Download a directory from S3.

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
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonStoresException:
            os.makedirs(local_path)

        results = self.list(bucket_name=bucket_name, prefix=key, delimiter='/')

        # Create directories
        for prefix in sorted(results['prefixes']):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(key, prefix)
            # Download files under
            self.download_dir(key=prefix,
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

    def delete(self, key, bucket_name=None):
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)

        results = self.list(bucket_name=bucket_name, prefix=key, delimiter='/')

        if not any([results['prefixes'], results['keys']]):
            self.delete_file(key=key, bucket_name=bucket_name)

        # Delete directories
        for prefix in sorted(results['prefixes']):
            prefix = os.path.join(key, prefix)
            # Download files under
            self.delete(key=prefix, bucket_name=bucket_name)

        # Delete files
        for file_key in results['keys']:
            file_key = file_key[0]
            file_key = os.path.join(key, file_key)
            self.delete_file(key=file_key, bucket_name=bucket_name)

    def delete_file(self, key, bucket_name=None):
        if not bucket_name:
            (bucket_name, key) = self.parse_s3_url(key)
        try:
            obj = self.resource.Object(bucket_name, key)
            obj.delete()
        except ClientError as e:
            raise PolyaxonStoresException(e)
