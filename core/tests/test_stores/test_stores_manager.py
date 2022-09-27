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
import pytest

from polyaxon import settings
from polyaxon.fs.async_manager import delete_file_or_dir, download_dir, download_file
from polyaxon.fs.fs import get_default_fs
from polyaxon.utils.path_utils import check_or_create_path
from polyaxon.utils.test_utils import create_tmp_files, set_store


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_download_dir_archive():
    store_root = set_store()
    path = os.path.join(store_root, "foo")
    check_or_create_path(path, is_dir=True)
    create_tmp_files(path)
    fs = await get_default_fs()
    await download_dir(fs=fs, subpath="foo", to_tar=True)

    path_to = os.path.join(settings.AGENT_CONFIG.local_root, "foo")
    assert os.path.exists(path_to)
    assert os.path.exists(path_to + "/file0.txt")
    assert os.path.exists(path_to + "/file1.txt")
    tar_path = os.path.join(settings.CLIENT_CONFIG.archive_root, "foo.tar.gz")
    assert os.path.exists(tar_path)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_download_file():
    store_root = set_store()
    path = os.path.join(store_root, "foo")
    check_or_create_path(path, is_dir=True)
    create_tmp_files(path)
    fs = await get_default_fs()
    await download_file(fs=fs, subpath="foo/file0.txt", check_cache=False)

    path_to = os.path.join(settings.AGENT_CONFIG.local_root, "foo/file0.txt")
    assert os.path.exists(path_to)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_delete_file():
    store_root = set_store()
    path = os.path.join(store_root, "foo")
    check_or_create_path(path, is_dir=True)
    create_tmp_files(path)
    filepath = "{}/file0.txt".format(path)
    assert os.path.exists(path) is True
    assert os.path.exists(filepath) is True
    fs = await get_default_fs()
    await delete_file_or_dir(fs=fs, subpath="foo/file0.txt", is_file=True)
    assert os.path.exists(path) is True
    assert os.path.exists(filepath) is False


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
async def test_delete_dir():
    store_root = set_store()
    path = os.path.join(store_root, "foo")
    check_or_create_path(path, is_dir=True)
    create_tmp_files(path)
    filepath = "{}/file0.txt".format(path)
    assert os.path.exists(path) is True
    assert os.path.exists(filepath) is True
    assert os.path.exists(filepath) is True
    fs = await get_default_fs()
    await delete_file_or_dir(fs=fs, subpath="foo", is_file=False)
    assert os.path.exists(path) is False
    assert os.path.exists(filepath) is False
