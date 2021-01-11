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
import shutil
import tarfile
import tempfile

from contextlib import contextmanager
from typing import List

from polyaxon.exceptions import PolyaxonPathException
from polyaxon.logger import logger
from polyaxon.utils import constants
from polyaxon.utils.list_utils import to_list


def get_path(store_path: str, entity_path: str) -> str:
    return os.path.join(store_path, entity_path)


def check_or_create_path(path: str = None, is_dir=False) -> None:
    if not is_dir:
        path = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(path):
        os.makedirs(path)


def delete_path(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except OSError:
        logger.warning("Could not delete path `%s`", path)


def create_path(path: str) -> None:
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.warning("Could not create path `%s`, exception %s", path, e)


def get_tmp_path(path: str) -> str:
    return get_path("/tmp", path)


def create_tmp_dir(dir_name: str) -> None:
    create_path(get_tmp_path(dir_name))


def delete_tmp_dir(dir_name: str) -> None:
    delete_path(get_tmp_path(dir_name))


def copy_to_tmp_dir(path: str, dir_name: str) -> str:
    tmp_path = get_tmp_path(dir_name)
    if os.path.exists(tmp_path):
        return tmp_path
    try:
        shutil.copytree(path, tmp_path)
    except FileExistsError as e:
        logger.warning("Path already exists `%s`, exception %s", path, e)
    return tmp_path


def copy_file(filename, path_to, use_basename=True):
    if use_basename:
        path_to = append_basename(path_to, filename)

    if filename == path_to:
        return

    check_or_create_path(path_to, is_dir=False)
    shutil.copy(filename, path_to)
    return path_to


@contextmanager
def get_files_by_paths(file_type, filepaths):
    local_files = []
    total_file_size = 0

    for filepath in filepaths:
        local_files.append(
            (file_type, (unix_style_path(filepath), open(filepath, "rb"), "text/plain"))
        )
        total_file_size += os.path.getsize(filepath)

    yield local_files, total_file_size

    # close all files to avoid WindowsError: [Error 32]
    for f in local_files:
        f[1][1].close()


def get_files_in_path(path: str, exclude: List[str] = None) -> List[str]:
    result_files = []
    for root, dirs, files in os.walk(path, topdown=True):
        exclude = to_list(exclude, check_none=True)
        if exclude:
            dirs[:] = [d for d in dirs if d not in exclude]
        logger.debug("Root:%s, Dirs:%s", root, dirs)
        for file_name in files:
            result_files.append(os.path.join(root, file_name))
    return result_files


def get_dirs_under_path(path: str) -> List[str]:
    return [
        name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
    ]


@contextmanager
def get_files_in_path_context(path: str, exclude: List[str] = None):
    """
    Gets all the files under a certain path.

    Args:
        path: `str`. The path to traverse for collecting files.
        exclude: `list`. List of paths to excludes.

    Returns:
         list of files collected under the path.
    """
    yield get_files_in_path(path, exclude=exclude)


def unix_style_path(path):
    if os.path.sep != "/":
        return path.replace(os.path.sep, "/")
    return path


def create_init_file():
    if os.path.exists(constants.INIT_FILE_PATH):
        return False

    with open(constants.INIT_FILE_PATH, "w") as f:
        f.write(constants.INIT_FILE_TEMPLATE)

    return True


def create_tarfile(files: List[str], tar_path: str, relative_to: str = None) -> None:
    """Create a tar file based on the list of files passed"""
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in files:
            arcname = os.path.relpath(f, relative_to) if relative_to else None
            tar.add(f, arcname=arcname)


@contextmanager
def create_tarfile_from_path(files, path_name, relative_to: str = None):
    """Create a tar file based on the list of files passed"""
    fd, filename = tempfile.mkstemp(prefix=path_name, suffix=".tar.gz")
    create_tarfile(files, filename, relative_to)
    yield filename

    # clear
    os.close(fd)
    os.remove(filename)


def untar_file(
    filename: str = None,
    delete_tar: bool = True,
    extract_path: str = None,
    use_filepath: bool = True,
):
    extract_path = extract_path or "."
    if use_filepath:
        extract_path = get_path(extract_path, filename.split(".tar.gz")[0])
    check_or_create_path(extract_path, is_dir=True)
    logger.info("Untarring the contents of the file ...")
    # Untar the file
    with tarfile.open(filename) as tar:
        tar.extractall(extract_path)
    if delete_tar:
        logger.info("Cleaning up the tar file ...")
        os.remove(filename)
    return extract_path


def move_recursively(src, dst):
    files = os.listdir(src)

    for f in files:
        shutil.move(os.path.join(src, f), dst)


def append_basename(path, filename):
    """
    Adds the basename of the filename to the path.

    Args:
        path: `str`. The path to append the basename to.
        filename: `str`. The filename to extract the base name from.

    Returns:
         str
    """
    return os.path.join(path, os.path.basename(filename))


def check_dirname_exists(path, is_dir=False):
    if not is_dir:
        path = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(path):
        raise PolyaxonPathException(
            "The parent path is not a directory {}".format(path)
        )


def create_polyaxon_tmp():
    base_path = os.path.join("/tmp", ".polyaxon")
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
        except OSError:
            # Except permission denied and potential race conditions
            # in multi-threaded environments.
            logger.warning("Could not create config directory `%s`", base_path)
    return base_path


def get_path_extension(filepath: str):
    return ".".join(os.path.basename(filepath).split(".")[1:]).lower()


def get_base_filename(filepath: str):
    return os.path.basename(filepath).split(".")[0]


def module_type(obj, type_pattern):
    the_type = type(obj)
    module = the_type.__module__
    name = the_type.__name__
    actual_fqn = "%s.%s" % (module, name)
    if isinstance(type_pattern, str):
        return type_pattern == actual_fqn
    else:
        return type_pattern.match(actual_fqn) is not None
