# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests
import os
import sys
import tarfile

from clint.textui import progress
from clint.textui.progress import Bar
from polyaxon_schemas.utils import to_list
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from polyaxon_client.logger import logger
from polyaxon_client.exceptions import ERRORS_MAPPING


class PolyaxonClient(object):
    """Base client for all HTTP operations."""
    ENDPOINT = None
    BASE_URL = "{}/api/{}/"
    MAX_UPLOAD_SIZE = 1024 * 1024 * 150
    PAGE_SIZE = 30

    def __init__(self,
                 host,
                 token=None,
                 version='v1',
                 authentication_type='token',
                 errors_mapping=ERRORS_MAPPING):
        self.base_url = self.BASE_URL.format(host, version)
        self.token = token
        self.authentication_type = authentication_type
        self.errors_mapping = errors_mapping

    @classmethod
    def get_page(cls, page=1):
        if page < 1:
            return ''
        return 'offset={}'.format((page - 1) * cls.PAGE_SIZE)

    @staticmethod
    def create_progress_callback(encoder):
        encoder_len = encoder.len
        bar = Bar(expected_size=encoder_len, filled_char='=')

        def callback(monitor):
            bar.show(monitor.bytes_read)

        return callback

    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        """
        Print in human friendly format
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    @staticmethod
    def _build_url(*parts):
        url = ''
        for part in parts:
            url += '{}/'.format(part.rstrip('/').lstrip('/'))

        return url

    def _get_url(self, endpoint=None):
        if not (endpoint or self.ENDPOINT):
            raise self.errors_mapping['base'](
                "This function expects `ENDPOINT` attribute to be set, "
                "or an `endpoint` argument to be passed.")
        endpoint = endpoint or self.ENDPOINT
        return self._build_url(self.base_url, endpoint)

    def _get_headers(self, headers=None):
        request_headers = headers or {}
        # Auth headers if access_token is present
        if self.token:
            request_headers.update({"Authorization": "{} {}".format(self.authentication_type,
                                                                    self.token)})
        return request_headers

    def request(self,
                method,
                url,
                params=None,
                data=None,
                files=None,
                json=None,
                timeout=5,
                headers=None):
        """Send a request with the given data as json to the given URL.

        Args:
            method: HTTP method
            url: The url to send the request to.
            params: Dictionary of values to format url.
            data:
            files:
            json:
            timeout:
            headers: extra headers to add to the request.

        Returns:
            Request response if successful, Exception otherwise.

        Raises:
            PolyaxonHTTPError or one of its subclasses.
        """
        logger.debug("Starting request to url: {} with params: {}, data: {}".format(
            url, params, data))

        request_headers = self._get_headers(headers=headers)

        try:
            response = requests.request(method,
                                        url,
                                        params=params,
                                        data=data,
                                        json=json,
                                        headers=request_headers,
                                        files=files,
                                        timeout=timeout)
        except requests.exceptions.ConnectionError as exception:
            logger.debug("Exception: %s", exception, exc_info=True)
            sys.exit("Cannot connect to the Polyaxon server. Check your internet connection.")

        logger.debug("Response Content: %s, Headers: %s" % (response.content, response.headers))
        self.check_response_status(response, url)
        return response

    def upload(self, url, files, files_size, params=None, json=None, timeout=3600):
        if files_size > self.MAX_UPLOAD_SIZE:
            sys.exit((
                "Files too large to sync, please keep it under {}.\n"
                "If you have data files in the current directory, "
                "please add them directly to your data volume, or upload them "
                "separately using `polyxon data` command and remove them from here.\n".format(
                    self.sizeof_fmt(self.MAX_UPLOAD_SIZE)
                )))

        files = to_list(files)
        if json:
            files.append(('json', json.dumps(json)))

        multipart_encoder = MultipartEncoder(
            fields=files
        )

        # Attach progress bar
        progress_callback, bar = self.create_progress_callback(multipart_encoder)
        multipart_encoder_monitor = MultipartEncoderMonitor(multipart_encoder, progress_callback)
        try:
            response = self.post(url=url,
                                 params=params,
                                 data=multipart_encoder_monitor,
                                 headers={"Content-Type": multipart_encoder.content_type},
                                 timeout=timeout)
        finally:
            # always make sure we clear the console
            bar.done()

        return response

    def download(self, url, filename, relative=False, headers=None, timeout=5):
        """
        Download the file from the given url at the current path
        """
        request_url = self.base_url + url if relative else url
        logger.debug("Downloading file from url: {}".format(request_url))

        request_headers = self._get_headers(headers=headers)

        try:
            response = requests.get(request_url,
                                    headers=request_headers,
                                    timeout=timeout,
                                    stream=True)
            self.check_response_status(response, request_url)
            with open(filename, 'wb') as f:
                # chunk mode response doesn't have content-length so we are
                # using a custom header here
                content_length = response.headers.get('x-polyaxon-content-length')
                if not content_length:
                    content_length = response.headers.get('content-length')
                if content_length:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                              expected_size=(int(content_length) / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                else:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            return filename
        except requests.exceptions.ConnectionError as exception:
            logger.debug("Exception: {}".format(exception))
            sys.exit("Cannot connect to the Polyaxon server. Check your internet connection.")

    def download_tar(self, url, untar=True, delete_after_untar=False):
        """
        Download and optionally untar the tar file from the given url
        """
        try:
            logger.info("Downloading the tar file to the current directory ...")
            filename = self.download(url=url, filename='output.tar')
            if filename and untar:
                logger.info("Untarring the contents of the file ...")
                tar = tarfile.open(filename)
                tar.extractall()
                tar.close()
            if delete_after_untar:
                logger.info("Cleaning up the tar file ...")
                os.remove(filename)
            return filename
        except self.errors_mapping['base'] as e:
            logger.info("Download URL ERROR! {}".format(e))
            return False

    def check_response_status(self, response, endpoint):
        """Check if response is successful. Else raise Exception."""

        if 200 <= response.status_code < 300:
            return response

        logger.error(
            "Request to {} failed with status code {}".format(endpoint, response.status_code),
            response.text)

        exception = self.errors_mapping.get(response.status_code, self.errors_mapping['http'])
        raise exception(endpoint=endpoint,
                        response=response,
                        message=response.text,
                        status_code=response.status_code)

    def get(self, url, params=None, data=None, files=None, json=None, timeout=5, headers=None):
        """Call request with a get."""
        return self.request('GET',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json,
                            timeout=timeout,
                            headers=headers)

    def post(self, url, params=None, data=None, files=None, json=None, timeout=5, headers=None):
        """Call request with a post."""
        return self.request('POST',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json,
                            timeout=timeout,
                            headers=headers)

    def patch(self, url, params=None, data=None, files=None, json=None, timeout=5, headers=None):
        """Call request with a patch."""
        return self.request('PATCH',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json,
                            timeout=timeout,
                            headers=headers)

    def delete(self, url, params=None, data=None, files=None, json=None, timeout=5, headers=None):
        """Call request with a delete."""
        return self.request('DELETE',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json,
                            timeout=timeout,
                            headers=headers)

    def put(self, url, params=None, data=None, files=None, json=None, timeout=5, headers=None):
        """Call request with a put."""
        return self.request('PUT',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json,
                            timeout=timeout,
                            headers=headers)
