# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import re

from six.moves import urllib

from azure.common import AzureMissingResourceHttpError
from azure.storage.blob.models import BlobPrefix

from polyaxon_stores.clients.azure_client import get_blob_service_connection
from polyaxon_stores.exceptions import PolyaxonStoresException


class AzureStore(object):
    def __init__(self, connection=None, **kwargs):
        self._connection = connection
        self._account_name = kwargs.get('account_name')
        self._account_key = kwargs.get('account_key')
        self._connection_string = kwargs.get('connection_string')

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

        :param account_name: The storage account name.
        :type account_name: str
        :param account_key: The storage account key.
        :type account_key: str
        :param connection_string: If specified, this will override all other parameters besides
        request session.
        :type connection_string: str

        :return: BlockBlobService instance
        """
        self._connection = get_blob_service_connection(account_name=account_name,
                                                       account_key=account_key,
                                                       connection_string=connection_string)

    @staticmethod
    def parse_wasbs_url(wasbs_url):
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

        :param blob: Name of existing blob.
        :type container_name: str
        :param container_name: Name of existing container.
        :type container_name: str
        :return: bool
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)
        try:
            return self.connection.get_blob_properties(
                container_name,
                blob
            )
        except AzureMissingResourceHttpError:
            return None

    def delete(self, blob, container_name=None):
        """
        Deletes if a blob exists.

        :param blob: Name of existing blob.
        :type container_name: str
        :param container_name: Name of existing container.
        :type container_name: str
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        try:
            self.connection.delete_blob(container_name, blob)
        except AzureMissingResourceHttpError:
            pass

    def list(self, key, container_name=None, path=None, delimiter='/', marker=None):
        """
        Checks if a blob exists.

        :param key: key prefix.
        :type container_name: str
        :param container_name: Name of existing container.
        :type container_name: str
        :param delimiter: the delimiter marks key hierarchy.
        :type delimiter: str
        :param marker: An opaque continuation token.
        :type delimiter: str
        :return:
        """
        if not container_name:
            container_name, _, key = self.parse_wasbs_url(key)

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
                    name = r.name[len(key) + 1:]
                    list_prefixes.append(name)
                else:
                    name = r.name[len(key) + 1:]
                    list_blobs.append((name, r.properties.content_length))
            if results.next_marker:
                marker = results.next_marker
            else:
                break
        return {
            'blobs': list_blobs,
            'prefixes': list_prefixes
        }

    def upload_file(self, blob, local_file, path=None, container_name=None):
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        key = blob
        if path:
            key = os.path.join(path, key)

        self.connection.create_blob_from_path(container_name, key, local_file)

    def download_file(self, blob, local_path, container_name=None):
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)
        self.connection.get_blob_to_path(container_name, blob, local_path)
