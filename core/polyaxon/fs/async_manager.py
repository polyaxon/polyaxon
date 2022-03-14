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

from typing import Dict, List, Optional, Union

import aiofiles

from starlette.concurrency import run_in_threadpool

from polyaxon import settings
from polyaxon.fs.tar import tar_dir
from polyaxon.fs.tar import tar_files as sync_tar_files
from polyaxon.fs.types import FSSystem
from polyaxon.logger import logger
from polyaxon.utils.hashing import hash_value
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.path_utils import check_or_create_path


async def ensure_async_execution(
    fs: FSSystem, fct: str, is_async: bool = False, *args, **kwargs
):
    async_fct = "_{}".format(fct)
    if is_async and hasattr(fs, async_fct):
        return await getattr(fs, async_fct)(*args, **kwargs)
    return await run_in_threadpool(getattr(fs, fct), *args, **kwargs)


async def upload_data(fs: FSSystem, subpath: str, data):
    path_to = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    try:
        return await ensure_async_execution(
            fs=fs,
            fct="pipe",
            is_async=fs.async_impl,
            path=path_to,
            value=data.encode(),
        )
    except Exception as e:
        logger.warning("Could not upload %s. Error %s" % (subpath, e))
        return None


async def upload_file(fs: FSSystem, subpath: str):
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_root, subpath)
    path_to = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    try:
        return await ensure_async_execution(
            fs=fs,
            fct="put",
            is_async=fs.async_impl,
            lpath=path_from,
            rpath=path_to,
            recursive=False,
        )
    except Exception as e:
        logger.warning("Could not upload %s. Error %s" % (path_from, e))
        return None


async def check_is_file(fs: FSSystem, subpath: str) -> bool:
    filepath = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    try:
        return await ensure_async_execution(
            fs=fs,
            fct="isfile",
            is_async=fs.async_impl,
            path=filepath,
        )
    except Exception as e:
        logger.warning(
            "Could not upload check the details of the path %s. Error %s"
            % (filepath, e)
        )
        return False


async def upload_dir(fs: FSSystem, subpath: str) -> Optional[str]:
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_root, subpath)
    path_to = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    try:
        return await ensure_async_execution(
            fs=fs,
            fct="put",
            is_async=fs.async_impl,
            lpath=path_from,
            rpath=path_to,
            recursive=True,
        )
    except Exception as e:
        logger.warning("Could not upload %s. Error %s" % (path_from, e))
        return None


async def download_file(
    fs: FSSystem, subpath: str, check_cache: bool = True
) -> Optional[str]:
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_to = os.path.join(settings.CLIENT_CONFIG.archive_root, subpath)

    if os.path.exists(path_to):
        if check_cache:
            # file already exists
            return path_to
        else:
            os.remove(path_to)

    try:
        check_or_create_path(path_to, is_dir=False)
    except Exception as e:
        logger.warning("Error during async dir creation. Error %s %s" % (path_from, e))
        pass
    try:
        await ensure_async_execution(
            fs=fs,
            fct="get",
            is_async=fs.async_impl,
            rpath=path_from,
            lpath=path_to,
            recursive=False,
        )
        return path_to
    except Exception as e:
        logger.warning("Could not download %s. Error %s" % (path_from, e))
        return None


async def download_files(
    fs: FSSystem,
    subpaths: List[str],
    check_cache: bool = True,
    pkg_files: List[str] = None,
) -> List[str]:
    pkg_files = to_list(pkg_files, check_none=True)
    for subpath in subpaths:
        try:
            file_to_path = await download_file(
                fs=fs, subpath=subpath, check_cache=check_cache
            )
            pkg_files.append(file_to_path)
        except Exception as e:
            logger.warning(
                "The file download for path %s failed. " "Error %s" % (subpath, e)
            )

    return pkg_files


async def open_file(
    fs: FSSystem, subpath: str, check_cache: bool = True
) -> Optional[str]:
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_to = os.path.join(settings.CLIENT_CONFIG.archive_root, subpath)

    if os.path.exists(path_to):
        if check_cache:
            # file already exists
            async with aiofiles.open(path_to, mode="r") as f:
                return await f.read()
        else:
            os.remove(path_to)

    try:
        check_or_create_path(path_to, is_dir=False)
    except Exception as e:
        logger.warning("Error during async dir creation. Error %s %s" % (path_from, e))
        pass
    try:
        content = await ensure_async_execution(
            fs=fs,
            fct="cat",
            is_async=fs.async_impl,
            path=path_from,
            recursive=False,
        )
        try:
            content = content.decode()
        except Exception as e:
            logger.warning("Could not decode content from bytes, error: %s", e)
        async with aiofiles.open(path_to, "w") as fw:
            await fw.write(content)
        return content
    except Exception as e:
        logger.warning("Could not download %s. Error %s" % (path_from, e))
        return None


async def download_dir(
    fs: FSSystem, subpath: str, to_tar: bool = False
) -> Optional[str]:
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_to = os.path.join(settings.CLIENT_CONFIG.archive_root, subpath)
    check_or_create_path(path_to, is_dir=True)
    try:
        await ensure_async_execution(
            fs=fs,
            fct="get",
            is_async=fs.async_impl,
            rpath=path_from,
            lpath=path_to,
            recursive=True,
        )
        if not os.path.exists(path_to):
            return None
        if to_tar:
            return await run_in_threadpool(tar_dir, path_to)
        return path_to
    except Exception as e:
        logger.warning("Could not download %s. Error %s" % (path_from, e))
        return None


async def download_dirs(
    fs: FSSystem,
    subpaths: List[str],
    pkg_files: List[str] = None,
    to_tar: bool = False,
    tar_filename: str = None,
) -> Union[str, List[str]]:
    pkg_files = to_list(pkg_files, check_none=True)
    for subpath in subpaths:
        try:
            file_to_path = await download_dir(fs=fs, subpath=subpath, to_tar=False)
            pkg_files.append(file_to_path)
        except Exception as e:
            logger.warning(
                "The file download for path %s failed. " "Error %s" % (subpath, e)
            )

    if to_tar:
        tar_filename = tar_filename or "download"
        return await tar_files(
            filename="{}.pkg.{}".format(tar_filename, hash_value(subpaths)),
            pkg_files=pkg_files,
            subpath=tar_filename,
        )
    return pkg_files


async def list_files(
    fs: FSSystem, subpath: str, filepath: str = None, force: bool = False
) -> Dict:
    store_path = os.path.join(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    if filepath:
        store_path = os.path.join(store_path, filepath)
    try:
        paths = await ensure_async_execution(
            fs=fs,
            fct="ls",
            is_async=fs.async_impl,
            path=store_path,
            detail=True,
            force=force,
        )
        results = {"files": {}, "dirs": []}
        for p in paths:
            name = os.path.basename(p["name"])
            if p.get("type") == "file":
                results["files"][name] = p.get("size")
            else:
                results["dirs"].append(name)
        return results
    except Exception as e:
        error = "Could not list path %s. Error %s" % (subpath, e)
        logger.warning(error)
        return {"files": {}, "dirs": [], "error": error}


async def delete_file_or_dir(
    fs: FSSystem, subpath: Union[str, List[str]], is_file: bool
) -> bool:
    try:
        await ensure_async_execution(
            fs=fs,
            fct="rm",
            is_async=fs.async_impl,
            path=os.path.join(
                settings.AGENT_CONFIG.artifacts_store.store_path, subpath
            ),
            recursive=not is_file,
        )
        return True
    except Exception as e:
        logger.warning("Could not delete %s. Error %s" % (subpath, e))
        return False


async def tar_files(filename: str, pkg_files: List[str], subpath: str = None) -> str:
    relative_to = (
        os.path.join(settings.CLIENT_CONFIG.archive_root, subpath) if subpath else None
    )
    return await run_in_threadpool(
        sync_tar_files,
        filename,
        pkg_files,
        relative_to,
    )
