# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tarfile
import tempfile

from contextlib import contextmanager

from polyaxon_cli.utils import constants


@contextmanager
def get_files_in_current_directory(file_type, file_paths):
    local_files = []
    total_file_size = 0

    for file_path in file_paths:
        local_files.append((file_type,
                            (unix_style_path(file_path), open(file_path, 'rb'), 'text/plain')))
        total_file_size += os.path.getsize(file_path)

    yield local_files, total_file_size

    # close all files to avoid WindowsError: [Error 32]
    for f in local_files:
        f[1][1].close()


def unix_style_path(path):
    if os.path.sep != '/':
        return path.replace(os.path.sep, '/')
    return path


def create_init_file(init_file_type):
    if os.path.exists(constants.INIT_FILE):
        return False

    with open(constants.INIT_FILE, 'w') as f:
        f.write(constants.INIT_FILE_TEMPLATES[init_file_type])

    return True


@contextmanager
def create_tarfile(files, project_name):
    """Create a tar file based on the list of files passed"""
    fd, filename = tempfile.mkstemp(prefix="polyaxon_{}".format(project_name), suffix='.tar.gz')
    with tarfile.open(filename, "w:gz") as tar:
        for f in files:
            tar.add(f)

    yield filename

    # clear
    os.close(fd)
    os.remove(filename)
