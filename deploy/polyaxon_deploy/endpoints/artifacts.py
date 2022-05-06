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

from starlette import status
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.routing import Route

from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.fs.async_manager import (
    check_is_file,
    delete_file_or_dir,
    download_dir,
    download_file,
    list_files,
)
from polyaxon.utils.bool_utils import to_bool
from polyaxon_deploy.connections.fs import AppFS
from polyaxon_deploy.controllers.notebooks import render_notebook
from polyaxon_deploy.controllers.uploads import handle_upload
from polyaxon_deploy.endpoints.base import UJSONResponse
from polyaxon_deploy.endpoints.utils import redirect_file


def clean_path(filepath: str):
    return filepath.strip("/")


async def handle_artifact(request: Request) -> Response:
    if request.method == "GET":
        return await download_artifact(request)
    if request.method == "DELETE":
        return await delete_artifact(request)
    if request.method == "POST":
        return await upload_artifact(request)


async def ro_artifact(request: Request) -> Response:
    path = request.path_params["path"]
    return await download_artifact(request, path, True)


async def download_artifact(
    request: Request, path: str = None, stream: bool = None
) -> Response:
    run_uuid = request.path_params["run_uuid"]
    filepath = request.query_params.get("path", path or "")
    stream = to_bool(request.query_params.get("stream", stream), handle_none=True)
    force = to_bool(request.query_params.get("force"), handle_none=True)
    render = to_bool(request.query_params.get("render"), handle_none=True)
    if not filepath:
        return Response(
            content="A `path` query param is required to stream a file content",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if render and not filepath.endswith(".ipynb"):
        return Response(
            content="Artifact with 'filepath={}' does not have a valid extension.".format(
                filepath
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    subpath = "{}/{}".format(run_uuid, clean_path(filepath)).rstrip("/")
    archived_path = await download_file(
        fs=await AppFS.get_fs(), subpath=subpath, check_cache=not force
    )
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}".format(archived_path),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if stream:
        if render:
            archived_path = await render_notebook(
                archived_path=archived_path, check_cache=not force
            )
        return FileResponse(archived_path, filename=os.path.basename(archived_path))
    return await redirect_file(archived_path)


async def upload_artifact(request: Request) -> Response:
    return await handle_upload(fs=await AppFS.get_fs(), request=request, is_file=True)


async def delete_artifact(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    filepath = request.query_params.get("path", "")
    if not filepath:
        return Response(
            content="A `path` query param is required to delete a file",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    subpath = "{}/{}".format(run_uuid, clean_path(filepath)).rstrip("/")
    is_deleted = await delete_file_or_dir(
        fs=await AppFS.get_fs(), subpath=subpath, is_file=True
    )
    if not is_deleted:
        return Response(
            content="Artifact could not be deleted: filepath={}".format(subpath),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


async def handle_artifacts(request: Request) -> Response:
    if request.method == "GET":
        return await download_artifacts(request)
    if request.method == "DELETE":
        return await delete_artifacts(request)
    if request.method == "POST":
        return await upload_artifacts(request)


async def download_artifacts(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    check_path = to_bool(request.query_params.get("check_path"), handle_none=True)
    if not check_path:
        # Backwards compatibility
        check_path = to_bool(request.query_params.get("check_file"), handle_none=True)
    path = request.query_params.get("path", "")
    subpath = "{}/{}".format(run_uuid, clean_path(path)).rstrip("/")
    fs = await AppFS.get_fs()
    if check_path:
        is_file = await check_is_file(fs=fs, subpath=subpath)
        if is_file:
            return await download_artifact(request)
    archived_path = await download_dir(fs=fs, subpath=subpath, to_tar=True)
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}".format(archived_path),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return await redirect_file(archived_path)


async def upload_artifacts(request: Request) -> Response:
    return await handle_upload(fs=await AppFS.get_fs(), request=request, is_file=False)


async def delete_artifacts(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    path = request.query_params.get("path", "")
    subpath = "{}/{}".format(run_uuid, clean_path(path)).rstrip("/")
    is_deleted = await delete_file_or_dir(
        fs=await AppFS.get_fs(), subpath=subpath, is_file=False
    )
    if not is_deleted:
        return Response(
            content="Artifacts could not be deleted: filepath={}".format(subpath),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


async def tree_artifacts(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    filepath = request.query_params.get("path", "")
    ls = await list_files(
        fs=await AppFS.get_fs(),
        subpath=run_uuid,
        filepath=clean_path(filepath),
        force=True,
    )
    return UJSONResponse(ls)


URLS_RUNS_ARTIFACT = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifact"
)
URLS_RUNS_EMBEDDED_ARTIFACT = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/embedded_artifact"
)
URLS_RUNS_RO_ARTIFACT = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/ro_artifact/{path:path}"
)
URLS_RUNS_ARTIFACTS = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifacts"
)
URLS_RUNS_ARTIFACTS_TREE = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifacts/tree"
)

# fmt: off
artifacts_routes = [
    Route(
        URLS_RUNS_ARTIFACT,
        handle_artifact,
        name="download_artifact",
        methods=["GET", "DELETE", "POST"],
    ),
    Route(
        URLS_RUNS_EMBEDDED_ARTIFACT,
        handle_artifact,
        name="download_embedded_artifact",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_RO_ARTIFACT,
        ro_artifact,
        name="read_only_artifact",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_ARTIFACTS,
        handle_artifacts,
        name="download_artifacts",
        methods=["GET", "DELETE", "POST"],
    ),
    Route(
        URLS_RUNS_ARTIFACTS_TREE,
        tree_artifacts,
        name="list_artifacts",
        methods=["GET"],
    ),
]
