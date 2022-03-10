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
from typing import Any, List, Union

from polyaxon.utils.list_utils import to_list
from polyaxon.utils.path_utils import get_files_in_path


def hash_value(value: Any, hash_length: int = 12) -> str:
    import hashlib

    return hashlib.md5(str(value).encode("utf-8")).hexdigest()[:hash_length]


def hash_file(
    filepath: str,
    hash_length: int = 12,
    chunk_size: int = 64 * 1024,
    hash_md5: Any = None,
    digest: bool = True,
) -> Union[any, str]:
    import hashlib

    hash_md5 = hash_md5 or hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()[:hash_length] if digest else hash_md5


def hash_files(
    filepaths: List[str],
    hash_length: int = 12,
    chunk_size: int = 64 * 1024,
    hash_md5: Any = None,
    digest: bool = True,
) -> Union[any, str]:
    import hashlib

    hash_md5 = hash_md5 or hashlib.md5()
    filepaths = to_list(filepaths, check_none=True)
    for filepath in filepaths:
        hash_md5 = hash_file(
            filepath=filepath,
            hash_length=hash_length,
            chunk_size=chunk_size,
            hash_md5=hash_md5,
            digest=False,
        )
    return hash_md5.hexdigest()[:hash_length] if digest else hash_md5


def hash_dir(
    dirpath: str,
    exclude: List[str] = None,
    hash_length: int = 12,
    chunk_size: int = 64 * 1024,
    hash_md5: Any = None,
    digest: bool = True,
) -> Union[any, str]:
    filepaths = get_files_in_path(path=dirpath, exclude=exclude)
    return hash_files(
        filepaths=filepaths,
        hash_length=hash_length,
        chunk_size=chunk_size,
        hash_md5=hash_md5,
        digest=digest,
    )
