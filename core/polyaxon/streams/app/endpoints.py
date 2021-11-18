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

from typing import Any, Dict

import ujson

from starlette import status
from starlette.background import BackgroundTask
from starlette.datastructures import QueryParams
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response

from polyaxon import settings
from polyaxon.fs.async_manager import (
    delete_file_or_dir,
    download_dir,
    download_file,
    list_files,
)
from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.k8s.logging.async_monitor import query_k8s_operation_logs
from polyaxon.lifecycle import V1StatusCondition
from polyaxon.logger import logger
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import V1Events
from polyaxon.streams.app.fs import AppFS
from polyaxon.streams.controllers.events import (
    get_archived_operation_events,
    get_archived_operation_resources,
    get_archived_operations_events,
)
from polyaxon.streams.controllers.k8s_check import k8s_check, reverse_k8s
from polyaxon.streams.controllers.k8s_crd import get_k8s_operation
from polyaxon.streams.controllers.k8s_pods import get_pods
from polyaxon.streams.controllers.logs import (
    get_archived_operation_logs,
    get_operation_logs,
    get_tmp_operation_logs,
)
from polyaxon.streams.controllers.notebooks import render_notebook
from polyaxon.streams.controllers.uploads import handle_upload
from polyaxon.streams.tasks.logs import clean_tmp_logs, upload_logs
from polyaxon.streams.tasks.notification import notify_run
from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.date_utils import parse_datetime
from polyaxon.utils.fqn_utils import get_resource_name, get_resource_name_for_kind
from polyaxon.utils.serialization import datetime_serialize


class UJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


async def health(request: Request) -> Response:
    return Response(status_code=status.HTTP_200_OK)


def clean_path(filepath: str):
    return filepath.strip("/")


async def get_logs(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    last_time = QueryParams(request.url.query).get("last_time")
    if last_time:
        last_time = parse_datetime(last_time).astimezone()
    last_file = QueryParams(request.url.query).get("last_file")
    files = []

    if last_time:
        resource_name = get_resource_name(run_uuid=run_uuid)

        k8s_manager = AsyncK8SManager(
            namespace=settings.CLIENT_CONFIG.namespace,
            in_cluster=settings.CLIENT_CONFIG.in_cluster,
        )
        await k8s_manager.setup()
        k8s_operation = await get_k8s_operation(
            k8s_manager=k8s_manager, resource_name=resource_name
        )
        if k8s_operation:
            operation_logs, last_time = await get_operation_logs(
                k8s_manager=k8s_manager,
                k8s_operation=k8s_operation,
                instance=run_uuid,
                last_time=last_time,
            )
        else:
            operation_logs, last_time = await get_tmp_operation_logs(
                fs=await AppFS.get_fs(), run_uuid=run_uuid, last_time=last_time
            )
        if k8s_manager:
            await k8s_manager.close()

    else:
        operation_logs, last_file, files = await get_archived_operation_logs(
            fs=await AppFS.get_fs(),
            run_uuid=run_uuid,
            last_file=last_file,
            check_cache=not force,
        )
    response = dict(
        last_time=datetime_serialize("last_time", {"last_time": last_time}),
        last_file=last_file,
        logs=operation_logs,
        files=files,
    )
    return UJSONResponse(response)


async def k8s_auth(request: Request) -> Response:
    uri = request.headers.get("x-origin-uri")
    if not uri:
        return Response(
            content="This endpoint can only be a sub-requested.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    try:
        path, params = k8s_check(uri)
    except ValueError as e:
        return Response(
            content="Error validating path. {}".format(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return await reverse_k8s(path="{}?{}".format(path, params))


async def k8s_inspect(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    resource_name = get_resource_name_for_kind(run_uuid=run_uuid)
    k8s_manager = AsyncK8SManager(
        namespace=settings.CLIENT_CONFIG.namespace,
        in_cluster=settings.CLIENT_CONFIG.in_cluster,
    )
    await k8s_manager.setup()
    k8s_operation = await get_k8s_operation(
        k8s_manager=k8s_manager, resource_name=resource_name
    )
    data = None
    if k8s_operation:
        data = await get_pods(k8s_manager=k8s_manager, run_uuid=run_uuid)
    if k8s_manager:
        await k8s_manager.close()
    return UJSONResponse(data or {})


async def collect_logs(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    run_kind = request.path_params["run_kind"]
    resource_name = get_resource_name_for_kind(run_uuid=run_uuid, run_kind=run_kind)
    k8s_manager = AsyncK8SManager(
        namespace=settings.CLIENT_CONFIG.namespace,
        in_cluster=settings.CLIENT_CONFIG.in_cluster,
    )
    await k8s_manager.setup()
    k8s_operation = await get_k8s_operation(
        k8s_manager=k8s_manager, resource_name=resource_name
    )
    if not k8s_operation:
        errors = "Run's logs was not collected, resource was not found."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    operation_logs, _ = await query_k8s_operation_logs(
        instance=run_uuid, k8s_manager=k8s_manager, last_time=None
    )
    if k8s_manager:
        await k8s_manager.close()
    if not operation_logs:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    try:
        await upload_logs(
            fs=await AppFS.get_fs(), run_uuid=run_uuid, logs=operation_logs
        )
    except Exception as e:
        errors = (
            "Run's logs was not collected, an error was raised while uploading the data %s."
            % e
        )
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if settings.AGENT_CONFIG.is_replica:
        task = BackgroundTask(clean_tmp_logs, run_uuid=run_uuid)
        return Response(background=task)
    return Response(status_code=status.HTTP_200_OK)


async def get_multi_run_events(request: Request) -> UJSONResponse:
    event_kind = request.path_params["event_kind"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    if event_kind not in V1ArtifactKind.allowable_values:
        raise HTTPException(
            detail="received an unrecognisable event {}.".format(event_kind),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    run_uuids = request.query_params["runs"]
    event_names = request.query_params["names"]
    orient = request.query_params.get("orient")
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    run_uuids = {e for e in run_uuids.split(",") if e} if run_uuids else set([])
    events = await get_archived_operations_events(
        fs=await AppFS.get_fs(),
        run_uuids=run_uuids,
        event_kind=event_kind,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


async def get_run_events(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    event_kind = request.path_params["event_kind"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    if event_kind not in V1ArtifactKind.allowable_values:
        raise HTTPException(
            detail="received an unrecognisable event {}.".format(event_kind),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    event_names = request.query_params["names"]
    orient = request.query_params.get("orient")
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    events = await get_archived_operation_events(
        fs=await AppFS.get_fs(),
        run_uuid=run_uuid,
        event_kind=event_kind,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


async def get_run_resources(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    event_names = request.query_params.get("names")
    orient = request.query_params.get("orient")
    force = to_bool(request.query_params.get("force"), handle_none=True)
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    events = await get_archived_operation_resources(
        fs=await AppFS.get_fs(),
        run_uuid=run_uuid,
        event_kind=V1ArtifactKind.METRIC,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


def inject_auth_header(request: Request, headers: Dict) -> Dict:
    auth = request.headers.get("Authorization")
    if auth:
        headers["Authorization"] = auth
    return headers


def _redirect(
    redirect_path: str, is_file: bool = False, additional_headers: Dict = None
) -> Response:

    headers = {"Content-Type": "", "X-Accel-Redirect": redirect_path}
    if additional_headers:
        headers.update(additional_headers)
    if is_file:
        headers["Content-Disposition"] = 'attachment; filename="{}"'.format(
            os.path.basename(redirect_path)
        )

    return Response(headers=headers)


def redirect_file(archived_path: str, additional_headers: Dict = None) -> Response:
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return _redirect(
        redirect_path=archived_path, is_file=True, additional_headers=additional_headers
    )


def redirect_api(redirect_path: str, additional_headers: Dict = None) -> Response:
    if not redirect_path:
        return Response(
            content="API not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return _redirect(
        redirect_path=redirect_path,
        is_file=False,
        additional_headers=additional_headers,
    )


async def notify(request: Request) -> Response:
    namespace = request.path_params["namespace"]
    owner = request.path_params["owner"]
    project = request.path_params["project"]
    run_uuid = request.path_params["run_uuid"]
    body = await request.json()
    run_name = body.get("name")
    condition = body.get("condition")
    if not condition:
        errors = "Received a notification request without condition."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    condition = V1StatusCondition.get_condition(**condition)
    connections = body.get("connections")
    if not connections:
        errors = "Received a notification request without connections."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.AGENT_CONFIG.connections:
        errors = "Received a notification request, but the agent did not declare connections."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    task = BackgroundTask(
        notify_run,
        namespace=namespace,
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        run_name=run_name,
        condition=condition,
        connections=connections,
    )
    return Response(background=task)


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
        return FileResponse(archived_path)
    return redirect_file(archived_path)


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
    path = request.query_params.get("path", "")
    subpath = "{}/{}".format(run_uuid, clean_path(path)).rstrip("/")
    archived_path = await download_dir(
        fs=await AppFS.get_fs(), subpath=subpath, to_tar=True
    )
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}".format(archived_path),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return redirect_file(archived_path)


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


async def error(request: Request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request: Request, exc) -> Response:
    """
    Return an HTTP 404 page.
    """
    return Response(status_code=status.HTTP_404_NOT_FOUND)


async def server_error(request: Request, exc):
    """
    Return an HTTP 500 page.
    """
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
