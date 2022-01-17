#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

import requests

from polyaxon import settings
from polyaxon.exceptions import (
    HTTP_ERROR_MESSAGES_MAPPING,
    PolyaxonClientException,
    PolyaxonShouldExitError,
)
from polyaxon.logger import logger


class HttpTransportMixin:
    """HTTP operations transport."""

    @property
    def session(self):
        if not hasattr(self, "_session"):
            self._session = requests.Session()
        return self._session

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        files=None,
        json=None,  # noqa
        timeout=None,
        headers=None,
        session=None,
    ):
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
        logger.debug(
            "Starting request to url: %s with params: %s, data: %s", url, params, data
        )

        request_headers = self._get_headers(headers=headers)
        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT
        session = session or self.session

        try:
            response = session.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                files=files,
                timeout=timeout,
                verify=self.config.verify_ssl,
            )
        except (
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exception:
            try:
                logger.debug("Exception: %s", exception, exc_info=True)
            except TypeError:
                pass
            raise PolyaxonShouldExitError(
                "Error connecting to Polyaxon server on `{}`.\n"
                "An Error `{}` occurred.\n"
                "Check your host and ports configuration "
                "and your internet connection.".format(url, exception)
            )

        logger.debug(
            "Response Content: %s, Headers: %s", response.content, response.headers
        )
        self.check_response_status(response, url)
        return response

    def check_response_status(self, response, endpoint):
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

    def get(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
    ):
        """Call request with a get."""
        return self.request(
            "GET",
            url=url,
            params=params,
            data=data,
            files=files,
            json=json_data,
            timeout=timeout,
            headers=headers,
            session=session,
        )

    def post(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
    ):
        """Call request with a post."""
        return self.request(
            "POST",
            url=url,
            params=params,
            data=data,
            files=files,
            json=json_data,
            timeout=timeout,
            headers=headers,
            session=session,
        )

    def patch(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
    ):
        """Call request with a patch."""
        return self.request(
            "PATCH",
            url=url,
            params=params,
            data=data,
            files=files,
            json=json_data,
            timeout=timeout,
            headers=headers,
            session=session,
        )

    def delete(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
    ):
        """Call request with a delete."""
        return self.request(
            "DELETE",
            url=url,
            params=params,
            data=data,
            files=files,
            json=json_data,
            timeout=timeout,
            headers=headers,
            session=session,
        )

    def put(
        self,
        url,
        params=None,
        data=None,
        files=None,
        json_data=None,
        timeout=None,
        headers=None,
        session=None,
    ):
        """Call request with a put."""
        return self.request(
            "PUT",
            url=url,
            params=params,
            data=data,
            files=files,
            json=json_data,
            timeout=timeout,
            headers=headers,
            session=session,
        )
