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

import ujson

from starlette import status
from starlette.datastructures import UploadFile
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from polyaxon import settings
from polyaxon.constants.globals import DEFAULT_UPLOADS_PATH
from polyaxon.stores.async_manager import upload_dir, upload_file
from polyaxon.utils.path_utils import check_or_create_path, delete_path, untar_file


async def handle_posted_data(
    content_file: UploadFile,
    root_path: str,
    path: str,
    upload: bool,
    is_file: bool,
    overwrite: bool = True,
    untar: bool = True,
) -> str:
    tmp_path = "{}/{}".format(
        root_path, os.path.basename(content_file.filename)
    ).rstrip("/")
    if path:
        root_path = "{}/{}".format(root_path, path).rstrip("/")
        if is_file:
            root_path = "{}/{}".format(
                root_path, os.path.basename(content_file.filename)
            )
    else:
        if untar:
            root_path = "{}/{}".format(root_path, DEFAULT_UPLOADS_PATH).rstrip("/")
        else:
            root_path = tmp_path
    if not untar:
        tmp_path = root_path
    full_tmppath = os.path.join(settings.AGENT_CONFIG.artifacts_root, tmp_path)
    full_filepath = os.path.join(settings.AGENT_CONFIG.artifacts_root, root_path)

    if overwrite and os.path.exists(full_filepath):
        delete_path(full_filepath)
    if not overwrite and os.path.exists(full_filepath):
        return full_filepath
    # Always clean tmp path
    if overwrite and os.path.exists(full_tmppath):
        delete_path(full_tmppath)

    check_or_create_path(full_tmppath, is_dir=False)
    check_or_create_path(full_filepath, is_dir=not is_file)

    # Creating the new file
    with open(full_tmppath, "wb") as destination:
        for chunk in content_file.file:
            destination.write(chunk)
    if untar:
        untar_file(full_tmppath, extract_path=full_filepath, use_filepath=False)
    if upload:
        if is_file:
            await upload_file(subpath=root_path)
        else:
            await upload_dir(subpath=root_path)
    return root_path


async def handle_upload(request: Request, is_file: bool) -> Response:
    form = await request.form()
    content_file = form["upload_file"]  # type: UploadFile
    content_json = form["json"]  # type: str
    content_json = ujson.loads(content_json) if content_json else {}
    run_uuid = request.path_params["run_uuid"]
    overwrite = content_json.get("overwrite", True)
    untar = content_json.get("untar", True)
    path = content_json.get("path", "")
    try:
        archived_path = await handle_posted_data(
            content_file=content_file,
            root_path=run_uuid,
            path=path,
            upload=True,
            is_file=is_file,
            overwrite=overwrite,
            untar=untar,
        )
    except Exception as e:
        raise HTTPException(
            detail="Run's artifacts upload was unsuccessful, "
            "an error was raised while uploading the data %s." % e,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not archived_path:
        return Response(
            content="Artifact not found and not uploaded: filepath={}".format(
                archived_path
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return Response(status_code=status.HTTP_200_OK)
