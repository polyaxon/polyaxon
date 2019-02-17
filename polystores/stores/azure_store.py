# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import re

from six.moves import urllib

from azure.common import AzureHttpError
from azure.storage.blob.models import BlobPrefix

from polystores.clients.azure_client import get_blob_service_connection
from polystores.exceptions import PolyaxonStoresException
from polystores.stores.base_store import BaseStore
from polystores.utils import append_basename, check_dirname_exists, get_files_in_current_directory

# pylint:disable=arguments-differ


class AzureStore(BaseStore):
    """
    Azure store Service.
    """
    STORE_TYPE = BaseStore._AZURE_STORE  # pylint:disable=protected-access

    def __init__(self, connection=None, **kwargs):
        self._connection = connection
        self._account_name = kwargs.get('account_name') or kwargs.get('AZURE_ACCOUNT_NAME')
        self._account_key = kwargs.get('account_key') or kwargs.get('AZURE_ACCOUNT_KEY')
        self._connection_string = (
            kwargs.get('connection_string') or kwargs.get('AZURE_CONNECTION_STRING'))

    @property
    def connection(self):
        if self._connection is None:
            self.set_connection(account_name=self._account_name,
                                account_key=self._account_key,
                                connection_string=self._connection_string)
        return self._connection

    def set_connection(self, account_name=None, account_key=None, connection_string=None):
        """
        Sets a new Blob service connection.

        Args:
        account_name: `str`. The storage account name.
        account_key: `str`. The storage account key.
        connection_string: `str`. If specified, this will override all other parameters besides
        request session.

        Returns:
            BlockBlobService instance
        """
        self._connection = get_blob_service_connection(account_name=account_name,
                                                       account_key=account_key,
                                                       connection_string=connection_string)

    def set_env_vars(self):
        if self._account_name:
            os.environ['AZURE_ACCOUNT_NAME'] = self._account_name
        if self._account_key:
            os.environ['AZURE_ACCOUNT_KEY'] = self._account_key
        if self._connection_string:
            os.environ['AZURE_CONNECTION_STRING'] = self._connection_string

    @staticmethod
    def parse_wasbs_url(wasbs_url):
        """
        Parses and validates a wasbs url.

        Returns:
            tuple(container, storage_account, path).
        """
        parsed_url = urllib.parse.urlparse(wasbs_url)
        if parsed_url.scheme != "wasbs":
            raise PolyaxonStoresException('Received an invalid url `{}`'.format(wasbs_url))
        match = re.match("([^@]+)@([^.]+)\\.blob\\.core\\.windows\\.net", parsed_url.netloc)
        if match is None:
            raise PolyaxonStoresException(
                'wasbs_url must be of the form <container>@<account>.blob.core.windows.net')
        container = match.group(1)
        storage_account = match.group(2)
        path = parsed_url.path
        if path.startswith('/'):
            path = path[1:]
        return container, storage_account, path

    def check_blob(self, blob, container_name=None):
        """
        Checks if a blob exists.

        Args:
            blob: `str`. Name of existing blob.
            container_name: `str`. Name of existing container.

        Returns:
            bool
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)
        try:
            return self.connection.get_blob_properties(
                container_name,
                blob
            )
        except AzureHttpError:
            return None

    def ls(self, path):
        results = self.list(key=path)
        return {'files': results['blobs'], 'dirs': results['prefixes']}

    def list(self, key, container_name=None, path=None, delimiter='/', marker=None):
        """
        Checks if a blob exists.

        Args:
            key: `str`. key prefix.
            container_name: `str`. Name of existing container.
            path: `str`. an extra path to append to the key.
            delimiter: `str`. the delimiter marks key hierarchy.
            marker: `str`. An opaque continuation token.
        """
        if not container_name:
            container_name, _, key = self.parse_wasbs_url(key)

        if key and not key.endswith('/'):
            key += '/'

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        if prefix and not prefix.endswith('/'):
            prefix += '/'

        list_blobs = []
        list_prefixes = []
        while True:
            results = self.connection.list_blobs(container_name,
                                                 prefix=prefix,
                                                 delimiter=delimiter,
                                                 marker=marker)
            for r in results:
                if isinstance(r, BlobPrefix):
                    name = r.name[len(key):]
                    list_prefixes.append(name)
                else:
                    name = r.name[len(key):]
                    list_blobs.append((name, r.properties.content_length))
            if results.next_marker:
                marker = results.next_marker
            else:
                break
        return {
            'blobs': list_blobs,
            'prefixes': list_prefixes
        }

    def upload_file(self, filename, blob, container_name=None, use_basename=True):
        """
        Uploads a local file to Google Cloud Storage.

        Args:
            filename: `str`. the file to upload.
            blob: `str`. blob to upload to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the filename.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        if use_basename:
            blob = append_basename(blob, filename)

        self.connection.create_blob_from_path(container_name, blob, filename)

    def upload_dir(self, dirname, blob, container_name=None, use_basename=True):
        """
        Uploads a local directory to to Google Cloud Storage.

        Args:
            dirname: `str`. name of the directory to upload.
            blob: `str`. blob to upload to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the directory.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        if use_basename:
            blob = append_basename(blob, dirname)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_current_directory(dirname) as files:
            for f in files:
                file_blob = os.path.join(blob, os.path.relpath(f, dirname))
                self.upload_file(filename=f,
                                 blob=file_blob,
                                 container_name=container_name,
                                 use_basename=False)

    def download_file(self, blob, local_path, container_name=None, use_basename=True):
        """
        Downloads a file from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the blob.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        check_dirname_exists(local_path)

        try:
            self.connection.get_blob_to_path(container_name, blob, local_path)
        except AzureHttpError as e:
            raise PolyaxonStoresException(e)

    def download_dir(self, blob, local_path, container_name=None, use_basename=True):
        """
        Download a directory from Google Cloud Storage.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the key.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonStoresException:
            os.makedirs(local_path)

        results = self.list(container_name=container_name, key=blob, delimiter='/')

        # Create directories
        for prefix in sorted(results['prefixes']):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.download_dir(blob=prefix,
                              local_path=direname,
                              container_name=container_name,
                              use_basename=False)

        # Download files
        for file_key in results['blobs']:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(blob, file_key)
            self.download_file(blob=file_key,
                               local_path=filename,
                               container_name=container_name,
                               use_basename=False)

    def delete(self, blob, container_name=None):
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        results = self.list(container_name=container_name, key=blob, delimiter='/')

        if not any([results['prefixes'], results['blobs']]):
            self.delete_file(blob=blob, container_name=container_name)

        # Delete directories
        for prefix in sorted(results['prefixes']):
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.delete(blob=prefix, container_name=container_name)

        # Delete files
        for file_key in results['blobs']:
            file_key = file_key[0]
            file_key = os.path.join(blob, file_key)
            self.delete_file(blob=file_key, container_name=container_name)

    def delete_file(self, blob, container_name=None):
        """
        Deletes if a blob exists.

        Args:
            blob: `str`. Name of existing blob.
            container_name: `str`. Name of existing container.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        try:
            self.connection.delete_blob(container_name, blob)
        except AzureHttpError:
            pass
