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

import sys

import click

from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError,
)
from polyaxon.logger import clean_outputs
from polyaxon.managers.ignore import IgnoreManager
from polyaxon.managers.project import ProjectManager
from polyaxon.utils.files import create_tarfile, get_files_in_current_directory
from polyaxon.utils.formatting import Printer


@click.command()
@clean_outputs
def upload(sync=True):  # pylint:disable=assign-to-new-keyword
    """Upload code of the current directory while respecting the .polyaxonignore file."""
    project = ProjectManager.get_config_or_raise()
    files = IgnoreManager.get_unignored_file_paths()
    try:
        with create_tarfile(files, project.name) as file_path:
            with get_files_in_current_directory("repo", [file_path]) as (
                files,
                files_size,
            ):
                try:
                    PolyaxonClient().project.upload_repo(
                        project.user, project.name, files, files_size, sync=sync
                    )
                except (
                    PolyaxonHTTPError,
                    PolyaxonShouldExitError,
                    PolyaxonClientException,
                ) as e:
                    Printer.print_error(
                        "Could not upload code for project `{}`.".format(project.name)
                    )
                    Printer.print_error("Error message `{}`.".format(e))
                    Printer.print_error(
                        "Check the project exists, "
                        "and that you have access rights, "
                        "this could happen as well when uploading large files. "
                        "Please also make sure that you have enough space to upload the data."
                    )
                    sys.exit(1)
                Printer.print_success("Files uploaded.")
    except Exception as e:
        Printer.print_error("Could not upload the file.")
        Printer.print_error("Error message `{}`.".format(e))
        sys.exit(1)
