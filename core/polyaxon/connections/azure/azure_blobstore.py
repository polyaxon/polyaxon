#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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
import logging
import os

from concurrent import futures
from typing import List, Optional

from azure.core.exceptions import HttpResponseError
from azure.storage.blob import BlobPrefix, BlobServiceClient

from polyaxon.connections.azure.base import (
    AzureService,
    get_account_key,
    get_account_name,
    get_connection_string,
)
from polyaxon.connections.reader import get_connection_context_path
from polyaxon.exceptions import (
    PolyaxonConnectionError,
    PolyaxonPathException,
    PolyaxonSchemaError,
    PolyaxonStoresException,
)
from polyaxon.parser import parser
from polyaxon.stores.base_store import StoreMixin
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.path_utils import (
    append_basename,
    check_dirname_exists,
    get_files_in_path_context,
)

logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure.storage.blob").setLevel(logging.WARNING)


def get_blob_service_connection(
    account_name=None,
    account_key=None,
    connection_string=None,
    context_path: Optional[str] = None,
):
    account_name = account_name or get_account_name(context_path=context_path)
    account_key = account_key or get_account_key(context_path=context_path)
    connection_string = connection_string or get_connection_string(
        context_path=context_path
    )
    if connection_string:
        return BlobServiceClient.from_connection_string(
            conn_str=connection_string, credential=account_key,
        )
    if account_name:
        return BlobServiceClient(
            account_url="https://{account}.blob.core.windows.net".format(
                account=account_name
            ),
            credential=account_key,
        )
    raise PolyaxonConnectionError(
        "Azure blob service connection requires an account name or a connection string"
    )


class AzureBlobStoreService(AzureService, StoreMixin):
    """
    Azure store Service.
    """

    @property
    def connection(self):
        if self._connection is None:
            self.set_connection(
                account_name=self._account_name,
                account_key=self._account_key,
                connection_string=self._connection_string,
            )
        return self._connection

    def set_connection(
        self,
        connection=None,
        connection_type=None,
        account_name=None,
        account_key=None,
        connection_string=None,
    ):
        """
        Sets a new Blob service connection.

        Args:
        account_name: `str`. The storage account name.
        account_key: `str`. The storage account key.
        connection_string: `str`. If specified, this will override all other parameters besides
        request session.

        Returns:
            BlobServiceClient instance
        """
        if connection:
            self._connection = connection
            return
        connection_type = connection_type or self._connection_type
        connection_name = connection_type.name if connection_type else None
        context_path = get_connection_context_path(name=connection_name)
        self._connection = get_blob_service_connection(
            account_name=account_name,
            account_key=account_key,
            connection_string=connection_string,
            context_path=context_path,
        )

    def set_env_vars(self):
        if self._account_name:
            os.environ["AZURE_ACCOUNT_NAME"] = self._account_name
        if self._account_key:
            os.environ["AZURE_ACCOUNT_KEY"] = self._account_key
        if self._connection_string:
            os.environ["AZURE_CONNECTION_STRING"] = self._connection_string

    @staticmethod
    def parse_wasbs_url(wasbs_url):
        """
        Parses and validates a wasbs url.

        Returns:
            tuple(container, storage_account, path).
        """
        try:
            spec = parser.parse_wasbs_path(wasbs_url)
            return spec.container, spec.storage_account, spec.path
        except PolyaxonSchemaError as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

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
            return self.connection.get_blob_properties(container_name, blob)
        except HttpResponseError:
            return None

    def ls(self, path):
        results = self.list(key=path)
        return {"files": results["blobs"], "dirs": results["prefixes"]}

    def list(self, key, container_name=None, path=None, delimiter="/", marker=None):
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

        client = self.connection.get_container_client(container_name)

        if key and not key.endswith("/"):
            key += "/"

        prefix = key
        if path:
            prefix = os.path.join(prefix, path)

        if prefix and not prefix.endswith("/"):
            prefix += "/"

        list_blobs = []
        list_prefixes = []
        results = client.walk_blobs(name_starts_with=prefix, delimiter=delimiter)
        for r in results:
            if isinstance(r, BlobPrefix):
                name = r.name[len(key) :]
                list_prefixes.append(name)
            else:
                name = r.name[len(key) :]
                list_blobs.append((name, r.size))
        return {"blobs": list_blobs, "prefixes": list_prefixes}

    def upload_file(self, filename, blob, container_name=None, use_basename=True):
        """
        Uploads a local file to Azure Blob service.

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

        client = self.connection.get_container_client(container_name)
        with open(filename, "rb") as file:
            client.upload_blob(blob, file, overwrite=True)

    def upload_dir(
        self,
        dirname,
        blob,
        container_name=None,
        use_basename=True,
        workers=0,
        last_time=None,
        exclude: List[str] = None,
    ):
        """
        Uploads a local directory to Azure Blob service.

        Args:
            dirname: `str`. name of the directory to upload.
            blob: `str`. blob to upload to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the directory.
            last_time: `datetime`. if provided,
                        it will only upload the file if changed after last_time.
            exclude: `list`. List of paths to exclude.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        if use_basename:
            blob = append_basename(blob, dirname)

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

                file_blob = os.path.join(blob, os.path.relpath(f, dirname))
                future_results = self.submit_pool(
                    workers=workers,
                    pool=pool,
                    future_results=future_results,
                    fn=self.upload_file,
                    filename=f,
                    blob=file_blob,
                    container_name=container_name,
                    use_basename=False,
                )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def download_file(self, blob, local_path, container_name=None, use_basename=True):
        """
        Downloads a file from Azure Blob service.

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

        try:
            check_dirname_exists(local_path)
        except PolyaxonPathException as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

        client = self.connection.get_container_client(container_name)
        try:
            with open(local_path, "wb") as file:
                client.download_blob(blob).readinto(file)
        except HttpResponseError as e:
            raise PolyaxonStoresException("Connection error: %s" % e) from e

    def download_dir(
        self, blob, local_path, container_name=None, use_basename=True, workers=0
    ):
        """
        Download a directory from Azure Blob service.

        Args:
            blob: `str`. blob to download.
            local_path: `str`. the path to download to.
            container_name: `str`. the name of the container.
            use_basename: `bool`. whether or not to use the basename of the key.
            workers: number of workers threads to use for parallel execution.
        """
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, blob)

        try:
            check_dirname_exists(local_path, is_dir=True)
        except PolyaxonPathException:
            os.makedirs(local_path)

        results = self.list(container_name=container_name, key=blob, delimiter="/")

        # Create directories
        for prefix in sorted(results["prefixes"]):
            direname = os.path.join(local_path, prefix)
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.download_dir(
                blob=prefix,
                local_path=direname,
                container_name=container_name,
                use_basename=False,
            )

        pool, future_results = self.init_pool(workers)

        # Download files
        for file_key in results["blobs"]:
            file_key = file_key[0]
            filename = os.path.join(local_path, file_key)
            file_key = os.path.join(blob, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.download_file,
                blob=file_key,
                local_path=filename,
                container_name=container_name,
                use_basename=False,
            )
        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def delete(self, blob, container_name=None, workers=0):
        if not container_name:
            container_name, _, blob = self.parse_wasbs_url(blob)

        results = self.list(container_name=container_name, key=blob, delimiter="/")

        if not any([results["prefixes"], results["blobs"]]):
            self.delete_file(blob=blob, container_name=container_name)

        # Delete directories
        for prefix in sorted(results["prefixes"]):
            prefix = os.path.join(blob, prefix)
            # Download files under
            self.delete(blob=prefix, container_name=container_name)

        pool, future_results = self.init_pool(workers)

        # Delete files
        for file_key in results["blobs"]:
            file_key = file_key[0]
            file_key = os.path.join(blob, file_key)
            future_results = self.submit_pool(
                workers=workers,
                pool=pool,
                future_results=future_results,
                fn=self.delete_file,
                blob=file_key,
                container_name=container_name,
            )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

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
            client = self.connection.get_container_client(container_name)
            client.delete_blob(blob)
        except HttpResponseError:
            pass
