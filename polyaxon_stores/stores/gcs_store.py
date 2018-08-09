# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from six.moves import urllib

from polyaxon_stores.clients import gc_client
from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.logger import logger


class GCSStore(object):
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

        :param project_id: The project if.
        :type project_id: str
        :param key_path: The path to the json key file.
        :type key_path: str
        :param keyfile_dict: The dict containing the auth data.
        :type keyfile_dict: str | dict
        :param credentials: The credentials to use.
        :type credentials: Credentials instance
        :param scopes: The scopes.
        :type scopes: list

        :return: Service client instance
        """
        self._client = gc_client.get_gc_client(
            project_id=project_id,
            key_path=key_path,
            keyfile_dict=keyfile_dict,
            credentials=credentials,
            scopes=scopes,
        )

    @staticmethod
    def parse_gcs_url(gcs_url):
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

        :param bucket_name: Name of the bucket
        :type bucket_name: str
        """
        return self.client.get_bucket(bucket_name)

    def delete(self, key, bucket_name=None):
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)
        bucket = self.get_bucket(bucket_name)
        bucket.delete_blob(key)

    def check_blob(self, blob, bucket_name=None):
        """
        Checks for the existence of a file in Google Cloud Storage.

        :param blob: the path to the object to check in the Google cloud storage bucket.
        :type blob: string
        :param bucket_name: Name of the bucket in which the file is stored
        :type bucket_name: str
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)
        try:
            self.client.objects().get(bucket=bucket_name, object=blob).execute()
            return True
        except Exception as e:
            logger.info('Block does not exist %s', e)
            return False

    def get_blob(self, blob, bucket_name=None):
        """
        Get a file in Google Cloud Storage.

        :param blob: the path to the object to check in the Google cloud storage bucket.
        :type blob: string
        :param bucket_name: Name of the bucket in which the file is stored
        :type bucket_name: str
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        bucket = self.get_bucket(bucket_name)
        # Wrap google.cloud.storage's blob to raise if the file doesn't exist
        obj = bucket.get_blob(blob)

        if obj is None:
            raise PolyaxonStoresException('File does not exist: {}'.format(blob))

        return obj

    def list(self, key, bucket_name=None, path=None, delimiter='/', blobs=True, prefixes=True):
        """
        List prefixes and blobs in a bucket.

        :param key: a key prefix.
        :type key: str
        :param bucket_name: the name of the bucket.
        :type bucket_name: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param blobs: if it should include blobs.
        :type blobs: bool
        :param prefixes: if it should include prefixes.
        :type prefixes: bool

        :return: Service client instance
        """
        if not bucket_name:
            bucket_name, key = self.parse_gcs_url(key)

        bucket = self.get_bucket(bucket_name)

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        # For bucket.list_blobs and logic below name needs to end in /
        # but for the root path "" we leave it as an empty string
        if prefix and not prefix.endswith('/'):
            prefix += '/'

        iterator = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

        def get_blobs(_blobs):
            list_blobs = []
            for blob in _blobs:
                name = blob.name[len(key) + 1:]
                list_blobs.append((name, blob.size))
            return list_blobs

        def get_prefixes(_prefixes):
            list_prefixes = []
            for folder_path in _prefixes:
                name = folder_path[len(key) + 1: -1]
                list_prefixes.append(name)
            return list_prefixes

        results = {
            'blobs': [],
            'prefixes': []
        }

        if blobs:
            results['blobs'] = get_blobs(list(iterator))

        if prefixes:
            for page in iterator.pages:
                results['prefixes'] = get_prefixes(page.prefixes)

        return results

    def download_file(self, blob, local_path, bucket_name=None):
        """
        Downloads a file from Google Cloud Storage.
        """
        if not bucket_name:
            (bucket_name, blob) = self.parse_gcs_url(blob)
        blob = self.get_blob(blob=blob, bucket_name=bucket_name)
        blob.download_to_filename(local_path)

    def upload_file(self, blob, filename, bucket_name=None):
        """
        Uploads a local file to Google Cloud Storage.
        """
        if not bucket_name:
            bucket_name, blob = self.parse_gcs_url(blob)

        obj = self.get_blob(blob, bucket_name)
        obj.upload_from_filename(filename)
