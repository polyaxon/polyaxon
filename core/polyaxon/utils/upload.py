#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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


def upload():
    """N.B. This is not available in all distributions.

    Upload code of the current directory while respecting the .polyaxonignore file.
    """
    import sys

    from polyaxon.cli.errors import handle_cli_error
    from polyaxon.client import PolyaxonClient
    from polyaxon.exceptions import (
        PolyaxonClientException,
        PolyaxonHTTPError,
        PolyaxonShouldExitError,
    )
    from polyaxon.managers.ignore import IgnoreConfigManager
    from polyaxon.managers.project import ProjectConfigManager
    from polyaxon.utils.formatting import Printer
    from polyaxon.utils.path_utils import create_project_tarfile, get_files_by_paths

    project = ProjectConfigManager.get_config_or_raise()
    files = IgnoreConfigManager.get_unignored_filepaths()
    try:
        with create_project_tarfile(files, project.name) as filepath:
            with get_files_by_paths("repo", [filepath]) as (files, files_size):
                try:
                    PolyaxonClient().project.upload_repo(
                        project.user, project.name, files, files_size
                    )
                except (
                    PolyaxonHTTPError,
                    PolyaxonShouldExitError,
                    PolyaxonClientException,
                ) as e:
                    handle_cli_error(
                        e,
                        message="Could not upload code for project `{}`.".format(
                            project.name
                        ),
                    )
                    Printer.print_error(
                        "Check that the project exists, "
                        "and that you have access rights, "
                        "this could happen as well when uploading large files. "
                        "Please also make sure that you have enough space to upload the data."
                    )
                    sys.exit(1)
                Printer.print_success("Files uploaded.")
    except Exception as e:
        handle_cli_error(e, message="Could not upload the file.")
        sys.exit(1)
