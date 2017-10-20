# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests
import os
import sys
import tarfile

from clint.textui import progress

from polyaxon_schemas.polyaxonfile.logger import logger

from polyaxon_cli.exceptions import ERRORS_MAPPING, PolyaxonHTTPError, PolyaxonException
from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager


class PolyaxonClient(object):
    """Base client for all HTTP operations."""
    ENDPOINT = None

    def __init__(self):
        self.base_url = "{}/api/v1/".format(GlobalConfigManager.get_value('host'))
        self.auth_config = AuthConfigManager.get_config()

    @staticmethod
    def _build_url(*parts):
        url = ''
        for part in parts:
            url = '{}/{}'.format(url, part.lstrip('/'))

        return url

    def _get_url(self, endpoint=None):
        if not (endpoint or self.ENDPOINT):
            raise PolyaxonException("This function expects `ENDPOINT` attribute to be set, "
                                    "or an `endpoint` argument to be passed.")
        endpoint = endpoint or self.ENDPOINT
        return self._build_url(self.base_url, endpoint)

    def _get_headers(self, headers=None):
        # Auth headers if access_token is present
        request_headers = {"Authorization": "Bearer {}".format(
            self.auth_config.token if self.auth_config else None),
        }
        # Add any additional headers
        if headers:
            request_headers.update(headers)

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
            url: The un-formatted url to send the request to.
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
        request_url = self._get_url(url)
        logger.debug("Starting request to url: {} with params: {}, data: {}".format(
            request_url, params, data))

        request_headers = self._get_headers(headers=headers)

        try:
            response = requests.request(method,
                                        request_url,
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
        self.check_response_status(response, request_url)
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
        except PolyaxonException as e:
            logger.info("Download URL ERROR! {}".format(e.message))
            return False

    @staticmethod
    def check_response_status(response, endpoint):
        """Check if response is successful. Else raise Exception."""

        if 200 <= response.status_code < 300:
            return response

        logger.error(
            "Request to {} failed with status code {}".format(endpoint, response.status_code),
            text=response.text)

        exception = ERRORS_MAPPING.get(response.status_code, PolyaxonHTTPError)
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
