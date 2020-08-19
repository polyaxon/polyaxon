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

import os
import requests

from polyaxon import settings
from polyaxon.client.transport.utils import progress_bar
from polyaxon.exceptions import (
    HTTP_ERROR_MESSAGES_MAPPING,
    PolyaxonClientException,
    PolyaxonShouldExitError,
)
from polyaxon.logger import logger
from polyaxon.stores.base_store import StoreMixin
from polyaxon.utils.path_utils import check_or_create_path, get_path, untar_file


class PolyaxonStore(StoreMixin):
    """
    Polyaxon filesystem store.

    Used to download data from Polyaxon streams apis.

    By default, this store requires a valid run.
    """

    URL = "streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/{subpath}"

    def __init__(self, client: "RunClient"):  # noqa
        self._client = client

    def ls(self, path):
        return self.list(path=path)

    def list(self, path):
        return self._client.get_artifacts_tree(path=path)

    def _get_headers(self, headers=None):
        request_headers = headers or {}
        # Auth headers if access_token is present
        if self._client.client.config:
            config = self._client.client.config
            if "Authorization" not in request_headers and config.token:
                request_headers.update(
                    {
                        "Authorization": "{} {}".format(
                            config.authentication_type, config.token
                        )
                    }
                )
            if config.header and config.header_service:
                request_headers.update({config.header: config.header_service})

        return request_headers

    @staticmethod
    def check_response_status(response, endpoint):
        """Check if response is successful. Else raise Exception."""

        if 200 <= response.status_code < 300:
            return response

        try:
            logger.error(
                "Request to %s failed with status code %s. \n" "Reason: %s",
                endpoint,
                response.status_code,
                response.text,
            )
        except TypeError:
            logger.error("Request to %s failed with status code", endpoint)

        raise PolyaxonClientException(
            HTTP_ERROR_MESSAGES_MAPPING.get(response.status_code)
        )

    def download(
        self,
        url,
        filename,
        params=None,
        headers=None,
        timeout=None,
        session=None,
        untar=False,
        delete_tar=True,
        extract_path=None,
    ):
        """
        Download the file from the given url at the current path
        """
        # pylint:disable=too-many-branches
        logger.debug("Downloading files from url: %s", url)

        request_headers = self._get_headers(headers=headers)
        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT
        session = session or requests.Session()

        try:
            response = session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=timeout,
                stream=True,
            )

            self.check_response_status(response, url)
            with open(filename, "wb") as f:
                # chunk mode response doesn't have content-length so we are
                # using a custom header here
                content_length = response.headers.get("x-polyaxon-content-length")
                if not content_length:
                    content_length = response.headers.get("content-length")
                if content_length:
                    for chunk in progress_bar(
                        response.iter_content(chunk_size=1024),
                        expected_size=(int(content_length) / 1024) + 1,
                    ):
                        if chunk:
                            f.write(chunk)
                else:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

            if untar:
                filename = untar_file(
                    filename=filename, delete_tar=delete_tar, extract_path=extract_path
                )
            return filename
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exception:
            try:
                logger.debug("Exception: %s", exception)
            except TypeError:
                pass

            raise PolyaxonShouldExitError(
                "Error connecting to Polyaxon server on `{}`.\n"
                "An Error `{}` occurred.\n"
                "Check your host and ports configuration "
                "and your internet connection.".format(url, exception)
            )

    def download_file(self, url, path, **kwargs):
        """This function downloads a single file a several files compressed in tar.gz.

        If the untar args is not specified it assumes a single file.
        If untar is provided: False or True it appends the tar.gz extension.
        If untar is True: it extracts the file.
        If untar is File: it keeps the file compressed.
        """
        local_path = kwargs.pop("path_to", None)
        local_path = local_path or get_path(
            settings.CLIENT_CONFIG.archive_root, self._client.run_uuid
        )
        if path:
            local_path = get_path(local_path, path)
        _local_path = local_path
        untar = kwargs.get("untar")
        if untar is not None:
            _local_path = _local_path + ".tar.gz"
        if untar is False:
            local_path = _local_path
        check_or_create_path(_local_path, is_dir=False)
        if not os.path.exists(_local_path):
            self.download(
                filename=_local_path, params={"path": path}, url=url, **kwargs
            )
        return local_path

    def upload_file(
        self, dirname, path_to, use_basename=True, workers=0, last_time=None
    ):
        pass

    def upload_dir(
        self, dirname, path_to, use_basename=True, workers=0, last_time=None
    ):
        pass

    def download_dir(
        self, path_from, local_path, use_basename=True, workers=0, **kwargs
    ):
        pass

    def delete(self, path, **kwargs):
        pass
