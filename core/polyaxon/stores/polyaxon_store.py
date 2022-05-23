#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
import json
import os
import requests

from typing import Dict, List

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from polyaxon import settings
from polyaxon.constants.globals import DEFAULT_UPLOADS_PATH
from polyaxon.env_vars.keys import EV_KEYS_UPLOAD_SIZE
from polyaxon.exceptions import (
    HTTP_ERROR_MESSAGES_MAPPING,
    PolyaxonClientException,
    PolyaxonShouldExitError,
)
from polyaxon.logger import logger
from polyaxon.utils.formatting import Printer
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.path_utils import (
    check_or_create_path,
    create_tarfile_from_path,
    get_files_by_paths,
    untar_file,
)
from traceml.processors.units_processors import format_sizeof


class PolyaxonStore:
    """
    Polyaxon filesystem store.

    Used to download data from Polyaxon streams apis.

    By default, this store requires a valid run.
    """

    def __init__(self, client: "RunClient"):  # noqa
        self._client = client

    def ls(self, path):
        return self.list(path=path)

    def list(self, path):
        return self._client.get_artifacts_tree(path=path)

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

    def upload(
        self,
        url,
        files,
        files_size,
        params=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
        show_progress=True,
    ):
        upload_size_max = os.environ.get(EV_KEYS_UPLOAD_SIZE)
        if not upload_size_max:
            # Backwards compatibility
            upload_size_max = os.environ.get("POLYAXON_UPLOAD_SIZE_MAX")
        if not upload_size_max:
            upload_size_max = 1024 * 1024 * 500
        try:
            upload_size_max = int(upload_size_max)
        except Exception as e:
            raise PolyaxonClientException("Could not parse max upload size") from e

        if files_size > 1024 * 1024 * 50:
            logger.warning(
                "You are uploading %s, there's a hard limit of %s.\n"
                "If you have data files in the current directory, "
                "please make sure to add them to .polyaxonignore or "
                "add them directly to your data volume, or upload them "
                "separately using `polyaxon data` command and remove them from here.\n",
                format_sizeof(files_size),
                format_sizeof(upload_size_max),
            )

        if files_size > upload_size_max:
            raise PolyaxonShouldExitError(
                "Files too large to sync, please keep it under {}.\n"
                "If you have data files in the current directory, "
                "please add them directly to your data volume, or upload them "
                "separately using `polyaxon data` command and remove them from here.\n".format(
                    format_sizeof(upload_size_max)
                )
            )

        files = to_list(files)
        if json_data:
            files.append(("json", json.dumps(json_data)))

        multipart_encoder = MultipartEncoder(fields=files)
        request_headers = self._client.client.config.get_full_headers(headers=headers)
        request_headers.update({"Content-Type": multipart_encoder.content_type})

        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT

        session = session or requests.Session()

        def _upload_impl(callback=None):
            multipart_encoder_monitor = MultipartEncoderMonitor(
                multipart_encoder, callback
            )
            return session.post(
                url=url,
                params=params,
                data=multipart_encoder_monitor,
                headers=request_headers,
                timeout=timeout,
            )

        if not show_progress:
            return _upload_impl()

        with Printer.get_progress() as progress:
            task = progress.add_task("[cyan]Uploading contents:", total=files_size)

            def progress_callback(monitor):
                progress.update(task, completed=monitor.bytes_read)

            return _upload_impl(progress_callback)

    def _get_header_value(self, headers: Dict, key: str):
        headers = headers or {}
        for k in headers.keys():
            kh = k.lower()
            if kh == key or kh == f"x-{key}":
                return headers.get(k, "")
        return ""

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
        use_filepath=True,
        show_progress=True,
    ):
        """
        Download the file from the given url at the current path
        """
        # pylint:disable=too-many-branches
        logger.debug("Downloading files from url: %s", url)

        request_headers = self._client.client.config.get_full_headers(headers=headers)
        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT
        session = session or requests.Session()

        try:
            with Printer.console.status("Loading content ..."):
                response = session.get(
                    url=url,
                    params=params,
                    headers=request_headers,
                    timeout=timeout,
                    stream=True,
                )
            content_disposition = self._get_header_value(
                headers=response.headers,
                key="content-disposition",
            )
            has_tar = (
                '.tar"' in content_disposition or '.tar.gz"' in content_disposition
            )
            if has_tar:
                filename = filename + ".tar.gz"
            if untar:
                untar = has_tar

            self.check_response_status(response, url)
            with open(filename, "wb") as f:
                content_length = self._get_header_value(
                    headers=response.headers,
                    key="content-length",
                )
                content_length = float(content_length) if content_length else None
                chunk_size = 1024 * 10

                def _download_impl():
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if progress:
                            progress.update(
                                task,
                                advance=len(chunk),
                            )
                        if chunk:
                            f.write(chunk)

                if show_progress:
                    with Printer.get_progress() as progress:
                        task = progress.add_task(
                            "Writing contents:", total=content_length
                        )
                        _download_impl()
                else:
                    _download_impl()

            if untar:
                filename = untar_file(
                    filename=filename,
                    delete_tar=delete_tar,
                    extract_path=extract_path,
                    use_filepath=use_filepath,
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
        """This function downloads a single file or several files compressed in tar.gz.

        If the untar args is not specified it assumes a single file.
        If untar is provided: False or True it appends the tar.gz extension.
        If untar is True: it extracts the file.
        If untar is False: it keeps the file compressed.
        """
        local_path = kwargs.pop("path_to", None)
        local_path = local_path or os.path.join(
            settings.CLIENT_CONFIG.archive_root, self._client.run_uuid
        )
        if path:
            local_path = os.path.join(local_path, path)

        check_or_create_path(local_path, is_dir=False)
        if not os.path.exists(local_path):
            params = kwargs.pop("params", {})
            params["path"] = path
            self.download(filename=local_path, params=params, url=url, **kwargs)
        return local_path

    def upload_file(
        self, url: str, filepath: str, show_progress: bool = True, **kwargs
    ):
        """This function uploads a single file or several files compressed in tar.gz.

        If the untar args is provided the server will decompress
        the uploaded file as a tar on the artifacts store.
        """
        json_data = {
            "untar": kwargs.get("untar", False),
            "path": kwargs.get("path", ""),
            "overwrite": kwargs.get("overwrite", True),
        }
        with get_files_by_paths("upload_file", [filepath]) as (files, files_size):
            return self.upload(
                url,
                files=files,
                files_size=files_size,
                json_data=json_data,
                show_progress=show_progress,
            )

    def upload_dir(self, url: str, files: List[str], **kwargs):
        path = kwargs.get("path", "")
        json_data = {
            "untar": True,
            "path": path,
            "overwrite": kwargs.get("overwrite", True),
        }
        dirname = os.path.basename(path) if path else DEFAULT_UPLOADS_PATH
        with create_tarfile_from_path(
            files, dirname, relative_to=kwargs.get("relative_to", None)
        ) as filepath:
            with get_files_by_paths("upload_file", [filepath]) as (files, files_size):
                return self.upload(
                    url, files=files, files_size=files_size, json_data=json_data
                )

    def download_dir(
        self, path_from, local_path, use_basename=True, workers=0, **kwargs
    ):
        pass

    def delete(self, path, **kwargs):
        pass
