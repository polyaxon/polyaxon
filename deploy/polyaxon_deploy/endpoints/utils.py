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
import os

from typing import Dict

from aiofiles.os import stat as aio_stat
from starlette import status
from starlette.requests import Request
from starlette.responses import FileResponse, Response

from polyaxon.services.values import PolyaxonServices


async def _redirect(
    redirect_path: str, is_file: bool = False, additional_headers: Dict = None
) -> Response:

    headers = {"Content-Type": "", "X-Accel-Redirect": redirect_path}
    if additional_headers:
        headers.update(additional_headers)
    if is_file:
        stat_result = await aio_stat(redirect_path)
        headers["X-Content-Length"] = str(stat_result.st_size)
        headers["Content-Disposition"] = 'attachment; filename="{}"'.format(
            os.path.basename(redirect_path)
        )

    return Response(headers=headers)


async def redirect_file(
    archived_path: str, additional_headers: Dict = None
) -> Response:
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if PolyaxonServices.is_sandbox():
        return FileResponse(archived_path, filename=os.path.basename(archived_path))
    return await _redirect(
        redirect_path=archived_path, is_file=True, additional_headers=additional_headers
    )


async def redirect_api(redirect_path: str, additional_headers: Dict = None) -> Response:
    if not redirect_path:
        return Response(
            content="API not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return await _redirect(
        redirect_path=redirect_path,
        is_file=False,
        additional_headers=additional_headers,
    )


def inject_auth_header(request: Request, headers: Dict) -> Dict:
    auth = request.headers.get("Authorization")
    if auth:
        headers["Authorization"] = auth
    return headers
