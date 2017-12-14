# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tarfile

from polyaxon_cli.utils import constants


def get_files_in_current_directory(file_type, file_paths):
    local_files = []
    total_file_size = 0

    for file_path in file_paths:
        local_files.append((file_type,
                            (unix_style_path(file_path), open(file_path, 'rb'), 'text/plain')))
        total_file_size += os.path.getsize(file_path)

    return local_files, total_file_size


def unix_style_path(path):
    if os.path.sep != '/':
        return path.replace(os.path.sep, '/')
    return path


def create_init_file(init_file_type, project=None):
    project = project or constants.INIT_FILE_PROJECT_SECTION
    if os.path.exists(constants.INIT_FILE):
        return False

    with open(constants.INIT_FILE, 'w') as f:
        f.write(constants.INIT_FILE_TEMPLATES[init_file_type].format(project))

    return True


def create_tarfile(files, project_name):
    """Create a tar file based on the list of files passed"""
    filename = "/tmp/{}.tar.gz".format(project_name)
    with tarfile.open(filename, "w:gz") as tar:
        for f in files:
            tar.add(f)

    return filename
