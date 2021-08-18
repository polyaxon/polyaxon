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
import asyncio
import os
import random
import requests.exceptions

import aiofiles
import aiohttp.client_exceptions
import google.auth.exceptions

from decorator import decorator
from gcsfs import GCSFileSystem as BaseGCSFileSystem
from gcsfs.checkers import get_consistency_checker
from gcsfs.retry import ChecksumError, HttpError, is_retriable, logger

from polyaxon.connections.gcp.base import get_gc_credentials, get_project_id


def validate_response(status, content, path):
    """
    Check the requests object r, raise error if it's not ok.

    Parameters
    ----------
    r: requests response object
    path: associated URL path, for error messages
    """
    if status >= 400:
        if status == 404:
            raise FileNotFoundError

        if hasattr(content, "decode"):
            content = content.decode()
        if status == 403:
            raise IOError("Forbidden: %s\n%s" % (path, content))
        elif status == 502:
            raise requests.exceptions.ProxyError()
        elif "invalid" in str(content):
            raise ValueError("Bad Request: %s\n%s" % (path, content))
        elif status:
            raise HttpError({"code": status, "message": content})  # text-like
        else:
            raise RuntimeError(content)


@decorator
async def retry_request(func, retries=6, *args, **kwargs):
    for retry in range(retries):
        try:
            if retry > 0:
                await asyncio.sleep(min(random.random() + 2 ** (retry - 1), 32))
            return await func(*args, **kwargs)
        except (
            HttpError,
            requests.exceptions.RequestException,
            google.auth.exceptions.GoogleAuthError,
            ChecksumError,
            aiohttp.client_exceptions.ClientError,
        ) as e:
            if (
                isinstance(e, HttpError)
                and e.code == 400
                and "requester pays" in e.message
            ):
                msg = (
                    "Bucket is requester pays. "
                    "Set `requester_pays=True` when creating the GCSFileSystem."
                )
                raise ValueError(msg) from e
            if isinstance(e, aiohttp.client_exceptions.ClientError) and e.code == 404:
                logger.debug("Request returned 404, no retries.")
                raise e
            if retry == retries - 1:
                logger.exception(
                    "%s out of retries on exception: %s" % (func.__name__, e)
                )
                raise e
            if is_retriable(e):
                logger.debug("%s retrying after exception: %s" % (func.__name__, e))
                continue
            logger.exception("%s non-retriable exception: %s" % (func.__name__, e))
            raise e


class GCSFileSystem(BaseGCSFileSystem):
    retries = 3

    @retry_request(retries=retries)
    async def _request(
        self, method, path, *args, headers=None, json=None, data=None, **kwargs
    ):
        await self._set_session()
        async with self.session.request(
            method=method,
            url=self._format_path(path, args),
            params=self._get_params(kwargs),
            json=json,
            headers=self._get_headers(headers),
            data=data,
            timeout=self.requests_timeout,
        ) as r:
            status = r.status
            headers = r.headers
            info = r.request_info  # for debug only
            contents = await r.read()

            validate_response(status, contents, path)
            return status, headers, info, contents

    @retry_request(retries=retries)
    async def _get_file_request(self, rpath, lpath, *args, headers=None, **kwargs):
        consistency = kwargs.pop("consistency", self.consistency)

        async with self.session.get(
            url=rpath,
            params=self._get_params(kwargs),
            headers=self._get_headers(headers),
            timeout=self.requests_timeout,
        ) as r:
            r.raise_for_status()
            checker = get_consistency_checker(consistency)

            os.makedirs(os.path.dirname(lpath), exist_ok=True)
            async with aiofiles.open(lpath, "wb") as f2:
                while True:
                    data = await r.content.read(4096 * 32)
                    if not data:
                        break
                    await f2.write(data)
                    checker.update(data)

            # validate http request
            validate_response(r.status, data, rpath)
            checker.validate_http_response(r)  # validate file consistency
            return r.status, r.headers, r.request_info, data


def get_fs(
    context_path: str = None,
    asynchronous: bool = False,
    use_listings_cache: bool = False,
    **kwargs
):

    return GCSFileSystem(
        project=get_project_id(context_path=context_path, **kwargs),
        token=get_gc_credentials(context_path=context_path, **kwargs),
        asynchronous=asynchronous,
        use_listings_cache=use_listings_cache,
    )
