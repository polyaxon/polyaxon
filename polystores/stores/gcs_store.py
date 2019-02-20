# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from six.moves import urllib

from google.api_core.exceptions import NotFound, GoogleAPIError

from polystores import settings
from polystores.clients import gc_client
from polystores.exceptions import PolyaxonStoresException
from polystores.logger import logger
from polystores.stores.base_store import BaseStore
from polystores.utils import (
    append_basename,
    check_dirname_exists,
    create_polyaxon_tmp,
    get_files_in_current_directory
)

# pylint:disable=arguments-differ


class GCSStore(BaseStore):
    """
    Google cloud store Service.
    """
    STORE_TYPE = BaseStore._GCS_STORE  # pylint:disable=protected-access

    def __init__(self, client=None, **kwargs):
        self._client = client
        self._project_id = kwargs.get('project_id')
        self._credentials = kwargs.get('credentials')
        self._key_path = kwargs.get('key_path')
        self._keyfile_dict = kwargs.get('keyfile_dict')
        self._scopes = kwargs.get('scopes')
        self._encoding = kwargs.get('encoding', 'utf-8')

    @property
    def client(self):
        if self._client is None:
            self.set_client(project_id=self._project_id,
                            key_path=self._key_path,
                            keyfile_dict=self._keyfile_dict,
                            scopes=self._scopes,
                            credentials=self._credentials)
        return self._client

    def set_client(self,
                   project_id=None,
                   key_path=None,
                   keyfile_dict=None,
                   credentials=None,
                   scopes=None):
        """
        Sets a new gc client.

        Args:
            project_id: `str`. The project if.
            key_path: `str`. The path to the json key file.
            keyfile_dict: `str`. The dict containing the auth data.
            credentials: `Credentials instance`. The credentials to use.
            scopes: `list`. The scopes.

        Returns:
            Service client instance
        """
        self._client = gc_client.get_gc_client(
            project_id=project_id,
            key_path=key_path,
            keyfile_dict=keyfile_dict,
            credentials=credentials,
            scopes=scopes,
        )

    def set_env_vars(self):
        if self._key_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self._key_path
        elif self._keyfile_dict:
            create_polyaxon_tmp()
            with open(settings.TMP_AUTH_GCS_ACCESS_PATH, 'w') as outfile:
                json.dump(self._keyfile_dict, outfile)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.TMP_AUTH_GCS_ACCESS_PATH

    @staticmethod
    def parse_gcs_url(gcs_url):
        """
        Parses and validates a google cloud storage url.

        Returns:
            tuple(bucket_name, blob).
        """
        parsed_url = urllib.parse.urlparse(gcs_url)
        if not parsed_url.netloc:
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(gcs_url))
        if parsed_url.scheme != 'gs':
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(gcs_url))
        blob = parsed_url.path.lstrip('/')
        return parsed_url.netloc, blob

    def get_bucket(self, bucket_name):
        """
        Gets a bucket by name.

        Args:
            bucket_name: `str`. Name of the bucket
        """
        return self.client.get_bucket(bucket_name)

    def check_blob(self, blob, bucket_name=None):
        """
        Checks for the existence of a file in Google Cloud Storage.

        Args:
            blob: `str`. the path to the object to check in the Google cloud storage bucket.
            bucket_name: `str`. Name of the bucket in which the file is stored
        """
        try:
            return bool(self.get_blob(blob=blob, bucket_name=bucket_name))
        except Exception as e:
            logger.info('Block does not exist %s', e)
            return False

    def get_blob(self, blob, bucket_name=None):
        """
        Get a file in Google Cloud Storage.

        Args:
            blob: `str`. the path to the object to check in the Google cloud storage bucket.
            bucket_name: `str`. Name of the bucket in which the file is stored
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        bucket = self.get_bucket(bucket_name)
        # Wrap google.cloud.storage's blob to raise if the file doesn't exist
        obj = bucket.get_blob(blob)

        if obj is None:
            raise PolyaxonStoresException('File does not exist: {}'.format(blob))

        return obj

    def ls(self, path):
        results = self.list(key=path)
        return {'files': results['blobs'], 'dirs': results['prefixes']}

    def list(self, key, bucket_name=None, path=None, delimiter='/', blobs=True, prefixes=True):
        """
        List prefixes and blobs in a bucket.

        Args:
            key: `str`. a key prefix.
            bucket_name: `str`. the name of the bucket.
            path: `str`. an extra path to append to the key.
            delimiter: `str`. the delimiter marks key hierarchy.
            blobs: `bool`. if it should include blobs.
            prefixes: `bool`. if it should include prefixes.

        Returns:
             Service client instance
        """
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        bucket = self.get_bucket(bucket_name)

        if key and not key.endswith('/'):
            key += '/'

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        if prefix and not prefix.endswith('/'):
            prefix += '/'

        def get_iterator():
            return bucket.list_blobs(prefix=prefix, delimiter=delimiter)

        def get_blobs(_blobs):
            list_blobs = []
            for blob in _blobs:
                name = blob.name[len(key):]
                size = blob.size
                if any([name, size]):
                    list_blobs.append((name, blob.size))
            return list_blobs

        def get_prefixes(_prefixes):
            list_prefixes = []
            for folder_path in _prefixes:
                name = folder_path[len(key): -1]
                list_prefixes.append(name)
            return list_prefixes

        results = {
            'blobs': [],
            'prefixes': []
        }

        if blobs:
            iterator = get_iterator()
            results['blobs'] = get_blobs(list(iterator))

        if prefixes:
            iterator = get_iterator()
            for page in iterator.pages:
                results['prefixes'] += get_prefixes(page.prefixes)

        return results

    def upload_file(self, filename, blob, bucket_name=None, use_basename=True):
        """
        Uploads a local file to Google Cloud Storage.

        Args:
            filename: `str`. the file to upload.
            blob: `str`. blob to upload to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the filename.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, filename)

        bucket = self.get_bucket(bucket_name)
        bucket.blob(blob).upload_from_filename(filename)

    def download_file(self, blob, local_path, bucket_name=None, use_basename=True):
        """
        Downloads a file from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the blob.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        check_dirname_exists(local_path)

        try:
            blob = self.get_blob(blob=blob, bucket_name=bucket_name)
            blob.download_to_filename(local_path)
        except (NotFound, GoogleAPIError) as e:
            raise PolyaxonStoresException(e)

    def upload_dir(self, dirname, blob, bucket_name=None, use_basename=True):
        """
        Uploads a local directory to to Google Cloud Storage.

        Args:
            dirname: `str`. name of the directory to upload.
            blob: `str`. blob to upload to.
            bucket_name: `str`. the name of the bucket.
            use_basename: `bool`. whether or not to use the basename of the directory.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        if use_basename:
            blob = append_basename(blob, dirname)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_current_directory(dirname) as files:
            for f in files:
                file_blob = os.path.join(blob, os.path.relpath(f, dirname))
                self.upload_file(filename=f,
                                 blob=file_blob,
                                 bucket_name=bucket_name,
                                 use_basename=False)

    def download_dir(self, blob, local_path, bucket_name=None, use_basename=True):
        """
        Download a directory from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            bucket_name: `str`. Name of the bucket in which to store the file.
            use_basename: `bool`. whether or not to use the basename of the key.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonStoresException:
            os.makedirs(local_path)

        results = self.list(bucket_name=bucket_name, key=blob, delimiter='/')

        # Create directories
        for prefix in sorted(results['prefixes']):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.download_dir(blob=prefix,
                              local_path=direname,
                              bucket_name=bucket_name,
                              use_basename=False)

        # Download files
        for file_key in results['blobs']:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(blob, file_key)
            self.download_file(blob=file_key,
                               local_path=filename,
                               bucket_name=bucket_name,
                               use_basename=False)

    def delete(self, key, bucket_name=None):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        results = self.list(bucket_name=bucket_name, key=key, delimiter='/')
        if not any([results['prefixes'], results['blobs']]):
            self.delete_file(key=key, bucket_name=bucket_name)

        # Delete directories
        for prefix in sorted(results['prefixes']):
            prefix = os.path.join(key, prefix)
            # Download files under
            self.delete(key=prefix, bucket_name=bucket_name)

        # Delete files
        for file_key in results['blobs']:
            file_key = file_key[0]
            file_key = os.path.join(key, file_key)
            self.delete_file(key=file_key, bucket_name=bucket_name)

    def delete_file(self, key, bucket_name=None):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)
        bucket = self.get_bucket(bucket_name)
        try:
            return bucket.delete_blob(key)
        except (NotFound, GoogleAPIError) as e:
            raise PolyaxonStoresException(e)
