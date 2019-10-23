#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tarfile
import tempfile

from contextlib import contextmanager

from polyaxon.utils import constants


@contextmanager
def get_files_in_current_directory(file_type, file_paths):
    local_files = []
    total_file_size = 0

    for file_path in file_paths:
        local_files.append(
            (
                file_type,
                (unix_style_path(file_path), open(file_path, "rb"), "text/plain"),
            )
        )
        total_file_size += os.path.getsize(file_path)

    yield local_files, total_file_size

    # close all files to avoid WindowsError: [Error 32]
    for f in local_files:
        f[1][1].close()


def unix_style_path(path):
    if os.path.sep != "/":
        return path.replace(os.path.sep, "/")
    return path


def create_init_file(init_file_type):
    if os.path.exists(constants.INIT_FILE_PATH):
        return False

    with open(constants.INIT_FILE_PATH, "w") as f:
        f.write(constants.PLX_FILE_TEMPLATES[init_file_type])

    return True


def create_debug_file(debug_file_type):
    if os.path.exists(constants.DEBUG_FILE_PATH):
        return False

    with open(constants.DEBUG_FILE_PATH, "w") as f:
        f.write(constants.PLX_FILE_TEMPLATES[debug_file_type])

    return True


@contextmanager
def create_tarfile(files, project_name):
    """Create a tar file based on the list of files passed"""
    fd, filename = tempfile.mkstemp(
        prefix="polyaxon_{}".format(project_name), suffix=".tar.gz"
    )
    with tarfile.open(filename, "w:gz") as tar:
        for f in files:
            tar.add(f)

    yield filename

    # clear
    os.close(fd)
    os.remove(filename)
