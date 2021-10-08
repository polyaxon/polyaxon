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
import os

import aiofiles

from gcsfs import GCSFileSystem as BaseGCSFileSystem
from gcsfs.checkers import get_consistency_checker
from gcsfs.retry import retry_request, validate_response

from polyaxon.connections.gcp.base import get_gc_credentials, get_project_id


class GCSFileSystem(BaseGCSFileSystem):
    retries = 3

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
